'''
Created on Apr 5, 2017

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

@author: michael
'''
import django
import endpoints
import logging
import MySQLdb
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from django.core.signals import request_finished
from protorpc import remote, messages
        
from api_3.cohort_endpoint_helpers import FilterDetails
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
    case_count = messages.IntegerField(11, variant=messages.Variant.INT32)
    sample_count = messages.IntegerField(12, variant=messages.Variant.INT32)
    cases = messages.StringField(13, repeated=True)
    samples = messages.StringField(14, repeated=True)

class CohortListDetails(messages.Message):
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
    case_count = messages.IntegerField(11, variant=messages.Variant.INT32)
    sample_count = messages.IntegerField(12, variant=messages.Variant.INT32)

class CohortDetailsList(messages.Message):
    items = messages.MessageField(CohortListDetails, 1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)

class CohortsGetListQueryBuilder(object):

    def build_cohort_query(self, query_dict):
        """
        Builds the query that will select cohort id, name, last_date_saved,
        perms, comments, source type, and source notes
        :param query_dict: should contain {'cohorts_cohort_perms.user_id': user_id, 'cohorts_cohort.active': unicode('1')}
        :return: query_str, query_tuple
        """
        query_str = 'SELECT cohorts_cohort.id, ' \
                    'cohorts_cohort.name, ' \
                    'cohorts_cohort.last_date_saved, ' \
                    'cohorts_cohort_perms.perm, ' \
                    'auth_user.email, ' \
                    'cohorts_cohort_comments.content AS comments, ' \
                    'cohorts_source.type AS source_type, ' \
                    'cohorts_source.notes AS source_notes ' \
                    'FROM cohorts_cohort_perms ' \
                    'JOIN cohorts_cohort ' \
                    'ON cohorts_cohort.id=cohorts_cohort_perms.cohort_id ' \
                    'JOIN auth_user ' \
                    'ON auth_user.id=cohorts_cohort_perms.user_id ' \
                    'LEFT JOIN cohorts_cohort_comments ' \
                    'ON cohorts_cohort_comments.user_id=cohorts_cohort_perms.user_id ' \
                    'AND cohorts_cohort_comments.cohort_id=cohorts_cohort.id ' \
                    'LEFT JOIN cohorts_source ' \
                    'ON cohorts_source.cohort_id=cohorts_cohort_perms.cohort_id '

        query_tuple = ()
        if query_dict:
            query_str += ' WHERE ' + '=%s and '.join(key for key in query_dict.keys()) + '=%s '
            query_tuple = tuple(value for value in query_dict.values())

        query_str += 'GROUP BY ' \
                     'cohorts_cohort.id,  ' \
                     'cohorts_cohort.name,  ' \
                     'cohorts_cohort.last_date_saved,  ' \
                     'cohorts_cohort_perms.perm,  ' \
                     'auth_user.email,  ' \
                     'comments,  ' \
                     'source_type,  ' \
                     'source_notes '

        return query_str, query_tuple

    def build_filter_query(self, filter_query_dict):
        """
        Builds the query that selects the filter name and value for a particular cohort
        :param filter_query_dict: should be {'cohorts_filters.resulting_cohort_id:': id}
        :return: filter_query_str, filter_query_tuple
        """
        filter_query_str = 'SELECT name, value ' \
                           'FROM cohorts_filters '

        filter_query_str += ' WHERE ' + '=%s AND '.join(key for key in filter_query_dict.keys()) + '=%s '
        filter_query_tuple = tuple(value for value in filter_query_dict.values())

        return filter_query_str, filter_query_tuple

    def build_parent_query(self, parent_query_dict):
        """
        Builds the query that selects parent_ids for a particular cohort
        :param parent_query_dict: should be {'cohort_id': str(row['id'])}
        :return: parent_query_str, parent_query_tuple
        """
        parent_query_str = 'SELECT parent_id ' \
                           'FROM cohorts_source '
        parent_query_str += ' WHERE ' + '=%s AND '.join(key for key in parent_query_dict.keys()) + '=%s '
        parent_query_tuple = tuple(value for value in parent_query_dict.values())

        return parent_query_str, parent_query_tuple

    def build_cases_query(self, case_query_dict):
        """
        Builds the query that selects the case count for a particular cohort
        :param case_query_dict: should be {'cohort_id': str(row['id])}
        :return: case_query_str, case_query_tuple
        """
        cases_query_str = 'SELECT cohort_id id, case_barcode ' \
                             'FROM cohorts_samples '

        cases_query_str += ' WHERE ' + '=%s AND '.join(key for key in case_query_dict.keys()) + '=%s '
        case_query_tuple = tuple(value for value in case_query_dict.values())

        return cases_query_str, case_query_tuple

    def build_samples_query(self, sample_query_dict):
        """
        Builds the query that selects the sample count for a particular cohort
        :param sample_query_dict: should be {'cohort_id': str(row['id])}
        :return: sample_query_str, sample_query_tuple
        """
        samples_query_str = 'SELECT sample_barcode, case_barcode ' \
                            'FROM cohorts_samples '

        samples_query_str += ' WHERE ' + '=%s AND '.join(key for key in sample_query_dict.keys()) + '=%s '
        sample_query_tuple = tuple(value for value in sample_query_dict.values())

        return samples_query_str, sample_query_tuple

class CohortsGetListMessageBuilder(object):
    def make_filter_details_from_cursor(self, filter_cursor_dict):
        """
        Returns list of FilterDetails from a dictionary of results
        from a filter query.
        """
        filter_data = []
        for filter_row in filter_cursor_dict:
            filter_data.append(FilterDetails(
                name=str(filter_row['name']),
                value=str(filter_row['value'])
            ))

        if len(filter_data) == 0:
            filter_data.append(FilterDetails(
                name="None",
                value="None"
            ))

        return filter_data

    def make_parent_id_list_from_cursor(self, parent_cursor_dict, row):
        """
        Returns list of parent_id's from a dictionary of results
        from a parent id query.
        """
        parent_id_data = [str(p_row['parent_id']) for p_row in parent_cursor_dict if row.get('parent_id')]
        if len(parent_id_data) == 0:
            parent_id_data.append("None")

        return parent_id_data

class CohortsGetListAPI(remote.Service):
    def validate_user(self):
        user_email = None
        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()
        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register "
                "with the web application.".
                format(BASE_URL))
        django.setup()
        try:
            user_id = Django_User.objects.get(email=user_email).id
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            logger.warn(e)
            request_finished.send(self)
            raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)
        return user_id,user_email

    def execute_getlist_query(self, param_map):
        query_str, query_tuple = CohortsGetListQueryBuilder().build_cohort_query(param_map)
        db = sql_connection()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query_str, query_tuple)
        return cursor, db

    def get_cohort_details(self, cursor, row):
        # get filters for each cohort
        filter_query_str, filter_query_tuple = CohortsGetListQueryBuilder().build_filter_query(
            {
                'cohorts_filters.resulting_cohort_id':str(row['id'])
            }
        )
        cursor.execute(filter_query_str, filter_query_tuple)
        filter_data = CohortsGetListMessageBuilder().make_filter_details_from_cursor(cursor.fetchall())

        # getting the parent_id's for each cohort is a separate query
        # since a single cohort may have multiple parent cohorts
        parent_query_str, parent_query_tuple = CohortsGetListQueryBuilder().build_parent_query(
            {
                'cohort_id':str(row['id'])
            }
        )
        cursor.execute(parent_query_str, parent_query_tuple)
        parent_id_data = CohortsGetListMessageBuilder().make_parent_id_list_from_cursor(
            cursor.fetchall(), row)

        # get number of cases for each cohort
        case_query_str, case_query_tuple = CohortsGetListQueryBuilder().build_cases_query(
            {
                'cohort_id':str(row['id'])
            }
        )
        cursor.execute(case_query_str, case_query_tuple)
        case_list = []
        for row in cursor.fetchall():
            case_list.append(row['case_barcode'])
        case_count = len(case_list)

        # get number of samples for each cohort
        sample_query_str, sample_query_tuple = CohortsGetListQueryBuilder().build_samples_query(
            {
                'cohort_id':str(row['id'])
            }
        )
        cursor.execute(sample_query_str, sample_query_tuple)
        sample_list = []
        for row in cursor.fetchall():
            sample_list.append(row['sample_barcode'])
        sample_count = len(sample_list)
        
        return parent_id_data, filter_data, case_list, case_count, sample_list, sample_count

class CohortsGetHelper(CohortsGetListAPI):
    GET_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True))

    def get(self, request):
        """
        Returns information about a specific cohort the user has READER or OWNER permission on
        when given a cohort ID. Authentication is required.
        """
        user_id, user_email = self.validate_user()

        cursor = None
        db = None
        cohort_id = request.get_assigned_value('cohort_id')
        param_map = {
            'cohorts_cohort_perms.user_id': user_id,
            'cohorts_cohort.active': unicode('1'),
            'cohorts_cohort.id': cohort_id
        }
        try:
            cursor, db = self.execute_getlist_query(param_map)
            row = cursor.fetchone()

            if row is None:
                raise endpoints.NotFoundException(
                    "Cohort {id} not found. Either it never existed, it was deleted, "
                    "or {user_email} does not have permission to view it.".format(
                        id=cohort_id, user_email=user_email))

            parent_id_data, filter_data, case_list, _, sample_list, _ = self.get_cohort_details(cursor, row)

            temp_list = []
            if len(sample_list) == 0:
                sample_list = ["None"]
            else:
                temp_list = []
                for sample in sample_list:
                    if sample is not None:
                        temp_list += [sample]
                sample_list = temp_list
                
            if len(case_list) == 0:
                case_list = ["None"]
            else:
                temp_list = []
                for case in case_list:
                    if case is not None:
                        temp_list += [case]
                case_list = temp_list

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
                case_count=len(case_list),
                sample_count=len(sample_list),
                cases=case_list,
                samples=sample_list
            )

        except (IndexError, TypeError) as e:
            raise endpoints.NotFoundException(
                "Cohort {} for user {} not found. {}: {}".format(cohort_id, user_email, type(e), e))

        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving cohorts or filters. {}".format(e))
            raise endpoints.BadRequestException("Error retrieving cohorts or filters. {}".format(e))

        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)

class CohortsListHelper(CohortsGetListAPI):
    def list(self, unused_request):
        """
        Returns information about cohorts a user has either READER or OWNER permission on.
        Authentication is required.
        """
        user_id, user_email = self.validate_user()

        param_map = {
            'cohorts_cohort_perms.user_id': user_id,
            'cohorts_cohort.active': unicode('1')
        }
        db = None
        cursor = None
        try:
            cursor, db = self.execute_getlist_query(param_map)
            data = []
            for row in cursor.fetchall():
                parent_id_data, filter_data, _, case_count, _, sample_count = self.get_cohort_details(cursor, row)
                
                data.append(
                    CohortListDetails(
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
                        case_count=case_count,
                        sample_count=sample_count
                    )
                )

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
