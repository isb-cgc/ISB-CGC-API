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

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from django.core.signals import request_finished
from protorpc import remote, messages, message_types

from isb_cgc_api_helpers import ISB_CGC_TARGET_Endpoints, CohortsGetListQueryBuilder, \
    CohortsGetListMessageBuilder, FilterDetails
from api_3.api_helpers import sql_connection

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class CohortDetails(messages.Message):
    id = messages.StringField(1)
    name = messages.StringField(2)
    last_date_saved = messages.StringField(3)
    permission = messages.StringField(4)
    email = messages.StringField(5)
    comments = messages.StringField(6)
    source_type = messages.StringField(7)
    source_notes = messages.StringField(8)
    parent_id = messages.StringField(9, repeated=True)
    filters = messages.MessageField(FilterDetails, 10, repeated=True)
    patient_count = messages.IntegerField(11, variant=messages.Variant.INT32)
    sample_count = messages.IntegerField(12, variant=messages.Variant.INT32)


class CohortDetailsList(messages.Message):
    items = messages.MessageField(CohortDetails, 1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)


@ISB_CGC_TARGET_Endpoints.api_class(resource_name='cohorts')
class CohortsListAPI(remote.Service):
    @endpoints.method(message_types.VoidMessage, CohortDetailsList, http_method='GET', path='cohorts')
    def list(self, unused_request):
        """
        Returns information about cohorts a user has either READER or OWNER permission on.
        Authentication is required. Optionally takes a cohort id as a parameter to
        only list information about one cohort.
        """
        user_email = None
        cursor = None
        db = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register "
                "with the web application.".format(BASE_URL))

        django.setup()
        try:
            user_id = Django_User.objects.get(email=user_email).id
        except (ObjectDoesNotExist, MultipleObjectsReturned), e:
            logger.warn(e)
            request_finished.send(self)
            raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)

        query_str, query_tuple = CohortsGetListQueryBuilder().build_cohort_query({
            'cohorts_cohort_perms.user_id': user_id,
            'cohorts_cohort.active': unicode('1')
        })

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)
            data = []

            for row in cursor.fetchall():
                # get filters for each cohort
                filter_query_str, filter_query_tuple = CohortsGetListQueryBuilder().build_filter_query(
                    {'cohorts_filters.resulting_cohort_id': str(row['id'])})
                cursor.execute(filter_query_str, filter_query_tuple)
                filter_data = CohortsGetListMessageBuilder().make_filter_details_from_cursor(
                    cursor.fetchall())

                # getting the parent_id's for each cohort is a separate query
                # since a single cohort may have multiple parent cohorts
                parent_query_str, parent_query_tuple = CohortsGetListQueryBuilder().build_parent_query(
                    {'cohort_id': str(row['id'])})
                cursor.execute(parent_query_str, parent_query_tuple)
                parent_id_data = CohortsGetListMessageBuilder().make_parent_id_list_from_cursor(
                    cursor.fetchall(), row)

                # get number of patients for each cohort
                patient_query_str, patient_query_tuple = CohortsGetListQueryBuilder().build_patients_query(
                    {'cohort_id': str(row['id'])})
                cursor.execute(patient_query_str, patient_query_tuple)
                patient_count = len(cursor.fetchall())

                # get number of samples for each cohort
                sample_query_str, sample_query_tuple = CohortsGetListQueryBuilder().build_samples_query(
                    {'cohort_id': str(row['id'])})
                cursor.execute(sample_query_str, sample_query_tuple)
                sample_count = len(cursor.fetchall())

                data.append(CohortDetails(
                    id=str(row['id']),
                    name=str(row['name']),
                    last_date_saved=str(row['last_date_saved']),
                    permission=str(row['perm']),
                    email=str(row['email']),
                    comments=str(row['comments']),
                    source_type=str(row['source_type']),
                    source_notes=str(row['source_notes']),
                    parent_id=parent_id_data,
                    filters=filter_data,
                    patient_count=patient_count,
                    sample_count=sample_count
                ))

            if len(data) == 0:
                raise endpoints.NotFoundException("{} has no active cohorts.".format(user_email))

            return CohortDetailsList(items=data, count=len(data))

        except (IndexError, TypeError) as e:
            raise endpoints.NotFoundException(
                "User {}'s cohorts not found. {}: {}".format(user_email, type(e), e))

        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving cohorts or filters. {}".format(e))
            raise endpoints.BadRequestException("Error retrieving cohorts or filters. {}".format(e))

        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)
