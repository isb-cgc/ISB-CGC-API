"""

Copyright 2015, Institute for Systems Biology

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
import endpoints
import logging
import MySQLdb
from protorpc import remote, messages
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from django.core.signals import request_finished
from isb_cgc_api_helpers import ISB_CGC_Endpoints, MetadataRangesItem, \
    are_there_bad_keys, are_there_no_acceptable_keys, construct_parameter_error_message
from api.api_helpers import sql_connection
from cohorts.models import Cohort as Django_Cohort, Cohort_Perms, Patients, Samples, Filters
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
        user_email = None
        patient_cursor = None
        sample_cursor = None
        db = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

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

        query_dict = {
            k.name: request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name)
            and k.name is not 'name'
            and not k.name.endswith('_gte')
            and not k.name.endswith('_lte')
            }

        gte_query_dict = {
            k.name.replace('_gte', ''): request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and k.name.endswith('_gte')
            }

        lte_query_dict = {
            k.name.replace('_lte', ''): request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and k.name.endswith('_lte')
            }

        patient_query_str = 'SELECT DISTINCT(IF(ParticipantBarcode="", LEFT(SampleBarcode,12), ParticipantBarcode)) ' \
                            'AS ParticipantBarcode ' \
                            'FROM metadata_samples ' \
                            'WHERE '

        sample_query_str = 'SELECT SampleBarcode ' \
                           'FROM metadata_samples ' \
                           'WHERE '
        value_tuple = ()

        for key, value_list in query_dict.iteritems():
            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            if "None" in value_list:
                value_list.remove("None")
                patient_query_str += ' ( {key} is null '.format(key=key)
                sample_query_str += ' ( {key} is null '.format(key=key)
                if len(value_list) > 0:
                    patient_query_str += ' OR {key} IN ({vals}) '.format(key=key,
                                                                         vals=', '.join(['%s'] * len(value_list)))
                    sample_query_str += ' OR {key} IN ({vals}) '.format(key=key,
                                                                        vals=', '.join(['%s'] * len(value_list)))
                patient_query_str += ') '
                sample_query_str += ') '
            else:
                patient_query_str += ' {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
                sample_query_str += ' {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
            value_tuple += tuple(value_list)

        for key, value in gte_query_dict.iteritems():
            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            patient_query_str += ' {} >=%s '.format(key)
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            sample_query_str += ' {} >=%s '.format(key)
            value_tuple += (value,)

        for key, value in lte_query_dict.iteritems():
            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            patient_query_str += ' {} <=%s '.format(key)
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            sample_query_str += ' {} <=%s '.format(key)
            value_tuple += (value,)

        sample_query_str += ' GROUP BY SampleBarcode'

        patient_barcodes = []
        sample_barcodes = []
        try:
            db = sql_connection()
            patient_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            patient_cursor.execute(patient_query_str, value_tuple)
            for row in patient_cursor.fetchall():
                patient_barcodes.append(row['ParticipantBarcode'])

            sample_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            sample_cursor.execute(sample_query_str, value_tuple)
            for row in sample_cursor.fetchall():
                sample_barcodes.append(row['SampleBarcode'])

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException("Error retrieving samples or patients")
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\tpatient query: {} {}\n\tsample query: {} {}' \
                .format(e, patient_query_str, value_tuple, sample_query_str, value_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error saving cohort. {}".format(msg))
        finally:
            if patient_cursor: patient_cursor.close()
            if sample_cursor: sample_cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)

        cohort_name = request.get_assigned_value('name')

        if len(patient_barcodes) == 0 or len(sample_barcodes) == 0:
            raise endpoints.BadRequestException(
                "The cohort could not be saved because no samples meet the specified parameters.")

        # todo: maybe create all objects first, then save them all at the end?
        # 1. create new cohorts_cohort with name, active=True, last_date_saved=now
        created_cohort = Django_Cohort.objects.create(name=cohort_name, active=True,
                                                      last_date_saved=datetime.utcnow())
        created_cohort.save()

        # 2. insert patients into cohort_patients
        patient_barcodes = list(set(patient_barcodes))
        patient_list = [Patients(cohort=created_cohort, patient_id=patient_code) for patient_code in
                        patient_barcodes]
        Patients.objects.bulk_create(patient_list)

        # 3. insert samples into cohort_samples
        sample_barcodes = list(set(sample_barcodes))
        sample_list = [Samples(cohort=created_cohort, sample_id=sample_code) for sample_code in sample_barcodes]
        Samples.objects.bulk_create(sample_list)

        # 4. Set permission for user to be owner
        perm = Cohort_Perms(cohort=created_cohort, user=django_user, perm=Cohort_Perms.OWNER)
        perm.save()

        # 5. Create filters applied
        filter_data = []
        for key, value_list in query_dict.items():
            for val in value_list:
                filter_data.append(FilterDetails(name=key, value=str(val)))
                Filters.objects.create(resulting_cohort=created_cohort, name=key, value=val).save()

        for key, val in [(k + '_lte', v) for k, v in lte_query_dict.items()] + [(k + '_gte', v) for k, v in gte_query_dict.items()]:
            filter_data.append(FilterDetails(name=key, value=str(val)))
            Filters.objects.create(resulting_cohort=created_cohort, name=key, value=val).save()

        # 6. Store cohort to BigQuery
        project_id = settings.BQ_PROJECT_ID
        cohort_settings = settings.GET_BQ_COHORT_SETTINGS()
        bcs = BigQueryCohortSupport(project_id, cohort_settings.dataset_id, cohort_settings.table_id)
        bcs.add_cohort_with_sample_barcodes(created_cohort.id, sample_barcodes)

        request_finished.send(self)
        return CreatedCohort(id=str(created_cohort.id),
                             name=cohort_name,
                             last_date_saved=str(datetime.utcnow()),
                             filters=filter_data,
                             patient_count=len(patient_barcodes),
                             sample_count=len(sample_barcodes)
                             )
