"""

Copyright 2016, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import django
import re
import endpoints
import logging
import MySQLdb
from protorpc import remote, messages
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from django.core.signals import request_finished
from isb_cgc_api_helpers import ISB_CGC_Endpoints, CohortsCreatePreviewQueryBuilder, \
    are_there_bad_keys, are_there_no_acceptable_keys, construct_parameter_error_message

from message_classes import MetadataRangesItem

from api_3.api_helpers import sql_connection, WHITELIST_RE
from cohorts.models import Cohort as Django_Cohort, Cohort_Perms, Samples, Filters
from bq_data_access.cohort_bigquery import BigQueryCohortSupport

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class FilterDetails(messages.Message):
    name = messages.StringField(1)
    value = messages.StringField(2)


class CreatedCohort(messages.Message):
    id = messages.StringField(1)
    name = messages.StringField(2)
    last_date_saved = messages.StringField(3)
    filters = messages.MessageField(FilterDetails, 4, repeated=True)
    patient_count = messages.IntegerField(5, variant=messages.Variant.INT32)
    sample_count = messages.IntegerField(6, variant=messages.Variant.INT32)


@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortsCreateAPI(remote.Service):
    POST_RESOURCE = endpoints.ResourceContainer(MetadataRangesItem,
                                                name=messages.StringField(2, required=True))

    @endpoints.method(POST_RESOURCE, CreatedCohort, path='cohorts/create', http_method='POST')
    def create(self, request):
        """
        Creates and saves a cohort. Takes a JSON object in the request body to use as the cohort's filters.
        Authentication is required.
        Returns information about the saved cohort, including the number of patients and the number
        of samples in that cohort.
        """
        cursor = None
        db = None

        user = endpoints.get_current_user()
        user_email = user.email() if user else None

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register "
                "with the web application.".format(BASE_URL))

        django.setup()
        try:
            django_user = Django_User.objects.get(email=user_email)
        except (ObjectDoesNotExist, MultipleObjectsReturned), e:
            logger.warn(e)
            request_finished.send(self)
            raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)

        if are_there_bad_keys(request) or are_there_no_acceptable_keys(request):
            err_msg = construct_parameter_error_message(request, True)
            request_finished.send(self)
            raise endpoints.BadRequestException(err_msg)

        query_dict, gte_query_dict, lte_query_dict = CohortsCreatePreviewQueryBuilder().build_query_dictionaries(request)

        patient_query_str, sample_query_str, value_tuple = CohortsCreatePreviewQueryBuilder().build_query(
            query_dict, gte_query_dict, lte_query_dict)

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sample_query_str, value_tuple)
            # TODO: We need to adjust this to pull the correct project ID as well
            sample_barcodes = [{'sample_barcode': row['sample_barcode'], 'case_barcode': row['case_barcode'], 'project_id': None,} for row in cursor.fetchall()]

        except (IndexError, TypeError), e:
            logger.warn(e)
            request_finished.send(self)
            raise endpoints.NotFoundException("Error retrieving samples or patients")
        except MySQLdb.ProgrammingError as e:
            logger.warn("Error saving cohort. {}".format(e))
            request_finished.send(self)
            raise endpoints.BadRequestException("Error saving cohort. {}".format(e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()

        cohort_name = request.get_assigned_value('name')

        # Validate the cohort name against a whitelist
        whitelist = re.compile(WHITELIST_RE, re.UNICODE)
        match = whitelist.search(unicode(cohort_name))
        if match:
            # XSS risk, log and fail this cohort save
            match = whitelist.findall(unicode(cohort_name))
            logger.error(
                '[ERROR] While saving a cohort, saw a malformed name: ' + cohort_name + ', characters: ' + match.__str__())
            raise endpoints.BadRequestException(
                "Your cohort's name contains invalid characters (" + match.__str__() + "); please choose another name.")

        if len(sample_barcodes) == 0:
            raise endpoints.BadRequestException(
                "The cohort could not be saved because no samples meet the specified parameters.")

        # todo: maybe create all objects first, then save them all at the end?
        # 1. create new cohorts_cohort with name, active=True, last_date_saved=now
        created_cohort = Django_Cohort.objects.create(name=cohort_name, active=True,
                                                      last_date_saved=datetime.utcnow())
        created_cohort.save()

        # 2. insert samples into cohort_samples
        sample_list = [Samples(cohort=created_cohort, sample_barcode=sample['sample_barcode'], case_barcode=sample['case_barcode'], project_id=sample['project_id']) for sample in sample_barcodes]
        Samples.objects.bulk_create(sample_list)

        # 3. Set permission for user to be owner
        perm = Cohort_Perms(cohort=created_cohort, user=django_user, perm=Cohort_Perms.OWNER)
        perm.save()

        # 4. Create filters applied
        filter_data = []
        for key, value_list in query_dict.items():
            for val in value_list:
                filter_data.append(FilterDetails(name=key, value=str(val)))
                Filters.objects.create(resulting_cohort=created_cohort, name=key, value=val).save()

        for key, val in [(k + '_lte', v) for k, v in lte_query_dict.items()] + [(k + '_gte', v) for k, v in gte_query_dict.items()]:
            filter_data.append(FilterDetails(name=key, value=str(val)))
            Filters.objects.create(resulting_cohort=created_cohort, name=key, value=val).save()

        # 5. Store cohort to BigQuery
        project_id = settings.BQ_PROJECT_ID
        cohort_settings = settings.GET_BQ_COHORT_SETTINGS()
        bcs = BigQueryCohortSupport(project_id, cohort_settings.dataset_id, cohort_settings.table_id)
        bcs.add_cohort_to_bq(created_cohort.id, sample_barcodes)

        request_finished.send(self)

        return CreatedCohort(id=str(created_cohort.id),
                             name=cohort_name,
                             last_date_saved=str(datetime.utcnow()),
                             filters=filter_data,
                             patient_count=created_cohort.case_size(),
                             sample_count=len(sample_barcodes)
                             )
