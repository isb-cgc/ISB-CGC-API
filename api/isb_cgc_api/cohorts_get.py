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
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints, CohortsGetListQueryBuilder
from api.api_helpers import sql_connection

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class FilterDetails(messages.Message):
    name = messages.StringField(1)
    value = messages.StringField(2)


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
    patients = messages.StringField(13, repeated=True)
    samples = messages.StringField(14, repeated=True)


@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortsGetAPI(remote.Service):
    GET_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True))

    @endpoints.method(GET_RESOURCE, CohortDetails, http_method='GET', path='cohorts/{cohort_id}')
    def get(self, request):
        """
        Returns information about cohorts a user has either READER or OWNER permission on.
        Authentication is required. Optionally takes a cohort id as a parameter to
        only list information about one cohort.
        """
        user_email = None
        cursor = None
        filter_cursor = None
        parent_cursor = None
        db = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        cohort_id = request.get_assigned_value('cohort_id')

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

        django.setup()
        try:
            user_id = Django_User.objects.get(email=user_email).id
        except (ObjectDoesNotExist, MultipleObjectsReturned), e:
            logger.warn(e)
            raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)

        query_dict = {'cohorts_cohort_perms.user_id': user_id, 'cohorts_cohort.active': unicode('1')}

        if cohort_id:
            query_dict['cohorts_cohort.id'] = cohort_id

        query_str, query_tuple = CohortsGetListQueryBuilder().build_cohort_query(query_dict)

        filter_query_str = ''
        parent_query_str = ''
        row = None

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)

            row = cursor.fetchone()
            if row is None:
                raise endpoints.NotFoundException(
                    "Cohort {id} not found. Either it never existed, it was deleted, "
                    "or {user_email} does not have permission to view it.".format(id=cohort_id, user_email=user_email))

            filter_query_dict = {'cohorts_filters.resulting_cohort_id': str(row['id'])}
            filter_query_str, filter_query_tuple = CohortsGetListQueryBuilder().build_filter_query(filter_query_dict)

            filter_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            filter_cursor.execute(filter_query_str, filter_query_tuple)
            filter_data = []
            for filter_row in filter_cursor.fetchall():
                filter_data.append(FilterDetails(
                    name=str(filter_row['name']),
                    value=str(filter_row['value'])
                ))

            if filter_data == []:
                filter_data.append(FilterDetails(
                    name="None",
                    value="None"
                ))

            # filter_data = CohortsListMessageListBuilder().build_message_list(FilterDetails,
            #                                                                  filter_cursor.fetchall())

            # getting the parent_id is a separate query since a single cohort
            # may have multiple parent cohorts
            parent_query_dict = {'cohort_id': str(row['id'])}
            parent_query_str, parent_query_tuple = CohortsGetListQueryBuilder().build_parent_query(parent_query_dict)

            parent_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            parent_cursor.execute(parent_query_str, parent_query_tuple)
            parent_id_data = [str(p_row['parent_id']) for p_row in parent_cursor.fetchall() if row.get('parent_id')]

            if parent_id_data == []:
                parent_id_data.append("None")

            patient_query_dict = {'cohort_id': str(row['id'])}
            patient_query_str, patient_query_tuple = CohortsGetListQueryBuilder().build_patients_query(patient_query_dict)
            cursor.execute(patient_query_str, patient_query_tuple)
            patient_list = [str(patient_row.get('patient_id')) for patient_row in cursor.fetchall() if patient_row.get('patient_id')]

            if patient_list == []:
                patient_list.append("None")

            sample_query_dict = {'cohort_id': str(row['id'])}
            sample_query_str, sample_query_tuple = CohortsGetListQueryBuilder().build_samples_query(sample_query_dict)
            cursor.execute(sample_query_str, sample_query_tuple)
            sample_list = [str(sample_row.get('sample_id')) for sample_row in cursor.fetchall() if sample_row.get('sample_id')]

            if sample_list == []:
                sample_list.append("None")


            return CohortDetails(
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
                patient_count=len(patient_list),
                sample_count=len(sample_list),
                patients=patient_list,
                samples=sample_list
            )

            # if len(data) == 0:
            #     # optional_message = " matching cohort id " + str(cohort_id) if cohort_id is not None else ""
            #     raise endpoints.NotFoundException("{} has no active cohorts.".format(user_email))
            # return CohortDetailsList(items=data, count=len(data))

        except (IndexError, TypeError) as e:
            raise endpoints.NotFoundException(
                "Cohort {} for user {} not found. {}: {}".format(cohort_id, user_email, type(e), e))

        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\tcohort query: {} {}\n\tfilter query: {} {}\n\tparent query: {} {}' \
                .format(e, query_str, query_tuple, filter_query_str, str(row['id']), parent_query_str,
                        str(row['id']))
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving cohorts or filters. {}".format(msg))

        finally:
            if cursor: cursor.close()
            if filter_cursor: filter_cursor.close()
            if parent_cursor: parent_cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)