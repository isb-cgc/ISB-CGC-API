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

import endpoints
import logging
import MySQLdb
import django

from django.conf import settings
from django.core.signals import request_finished
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints
from api_3.api_helpers import sql_connection
from cohorts.models import Cohort as Django_Cohort, Cohort_Perms

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class GoogleGenomics(messages.Message):
    SampleBarcode = messages.StringField(1)
    GG_dataset_id = messages.StringField(2)
    GG_readgroupset_id = messages.StringField(3)


class GoogleGenomicsList(messages.Message):
    items = messages.MessageField(GoogleGenomics, 1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)


# @ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortsGoogleGenomicssAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True))

    # @endpoints.method(GET_RESOURCE, GoogleGenomicsList, http_method='GET',
    #                   path='cohorts/{cohort_id}/googlegenomics')
    def googlegenomics(self, request):
        """
        Returns a list of Google Genomics dataset and readgroupset ids associated with
        all the samples in a specified cohort.
        Authentication is required. User must have either READER or OWNER permissions on the cohort.
        """
        cursor = None
        db = None
        user_email = None
        cohort_id = request.get_assigned_value('cohort_id')

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

        django.setup()
        try:
            user_id = Django_User.objects.get(email=user_email).id
            Django_Cohort.objects.get(id=cohort_id)
            Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user_id)
        except (ObjectDoesNotExist, MultipleObjectsReturned), e:
            logger.warn(e)
            err_msg = "Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e)
            if 'Cohort_Perms' in e.message:
                err_msg = "User {} does not have permissions on cohort {}. Error: {}" \
                    .format(user_email, cohort_id, e)
            request_finished.send(self)
            raise endpoints.UnauthorizedException(err_msg)

        query_str = 'SELECT SampleBarcode, GG_dataset_id, GG_readgroupset_id ' \
                    'FROM metadata_data ' \
                    'JOIN cohorts_samples ON metadata_data.SampleBarcode=cohorts_samples.sample_barcode ' \
                    'WHERE cohorts_samples.cohort_id=%s ' \
                    'AND GG_dataset_id !="" AND GG_readgroupset_id !="" ' \
                    'GROUP BY SampleBarcode, GG_dataset_id, GG_readgroupset_id;'

        query_tuple = (cohort_id,)
        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)

            google_genomics_items = [
                GoogleGenomics(
                        SampleBarcode=row['SampleBarcode'],
                        GG_dataset_id=row['GG_dataset_id'],
                        GG_readgroupset_id=row['GG_readgroupset_id']
                    )
                for row in cursor.fetchall()
            ]

            return GoogleGenomicsList(items=google_genomics_items, count=len(google_genomics_items))

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException(
                "Google Genomics dataset and readgroupset id's for cohort {} not found."
                    .format(cohort_id))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\tquery: {} {}' \
                .format(e, query_str, query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving genomics data for cohort. {}".format(msg))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)