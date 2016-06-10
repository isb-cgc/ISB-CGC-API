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

from isb_cgc_api_helpers import ISB_CGC_Endpoints, MetadataRangesItem, \
    are_there_bad_keys, are_there_no_acceptable_keys, construct_parameter_error_message
from api.api_helpers import sql_connection, get_user_email_from_token

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class CohortPatientsSamplesList(messages.Message):
    patients = messages.StringField(1, repeated=True)
    patient_count = messages.IntegerField(2)
    samples = messages.StringField(3, repeated=True)
    sample_count = messages.IntegerField(4)
    cohort_id = messages.IntegerField(5)


class FilterDetails(messages.Message):
    name = messages.StringField(1)
    value = messages.StringField(2)


class CohortDetails(messages.Message):
    id = messages.StringField(1)
    name = messages.StringField(2)
    last_date_saved = messages.StringField(3)
    perm = messages.StringField(4)
    email = messages.StringField(5)
    comments = messages.StringField(6)
    source_type = messages.StringField(7)
    source_notes = messages.StringField(8)
    parent_id = messages.IntegerField(9, repeated=True)
    filters = messages.MessageField(FilterDetails, 10, repeated=True)
    num_patients = messages.StringField(11)
    num_samples = messages.StringField(12)


class CohortDetailsList(messages.Message):
    items = messages.MessageField(CohortDetails, 1, repeated=True)
    count = messages.IntegerField(2)


class CohortsListQueryBuilder(object):

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


@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortAPI(remote.Service):
    GET_RESOURCE = endpoints.ResourceContainer(token=messages.StringField(1), cohort_id=messages.IntegerField(2))

    @endpoints.method(GET_RESOURCE, CohortDetailsList, http_method='GET')
    def list(self, request):
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

        # users have the option of pasting the access token in the query string
        # or in the 'token' field in the api explorer
        # but this is not required
        access_token = request.get_assigned_value('token')
        if access_token:
            user_email = get_user_email_from_token(access_token)

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

        query_str, query_tuple = CohortsListQueryBuilder().build_cohort_query(query_dict)

        filter_query_str = ''
        parent_query_str = ''
        row = None

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)
            data = []

            for row in cursor.fetchall():
                filter_query_dict = {'cohorts_filters.resulting_cohort_id': str(row['id'])}
                filter_query_str, filter_query_tuple = CohortsListQueryBuilder().build_filter_query(filter_query_dict)

                filter_cursor = db.cursor(MySQLdb.cursors.DictCursor)
                filter_cursor.execute(filter_query_str, filter_query_tuple)
                filter_data = []
                for filter_row in filter_cursor.fetchall():
                    filter_data.append(FilterDetails(
                        name=str(filter_row['name']),
                        value=str(filter_row['value'])
                    ))

                # filter_data = CohortsListMessageListBuilder().build_message_list(FilterDetails,
                #                                                                  filter_cursor.fetchall())

                # getting the parent_id is a separate query since a single cohort
                # may have multiple parent cohorts
                parent_query_dict = {'cohort_id': str(row['id'])}
                parent_query_str, parent_query_tuple = CohortsListQueryBuilder().build_parent_query(parent_query_dict)

                parent_cursor = db.cursor(MySQLdb.cursors.DictCursor)
                parent_cursor.execute(parent_query_str, parent_query_tuple)
                parent_id_data = [int(p_row['parent_id']) for p_row in parent_cursor.fetchall() if row.get('parent_id')]

                data.append(CohortDetails(
                    id=str(row['id']),
                    name=str(row['name']),
                    last_date_saved=str(row['last_date_saved']),
                    perm=str(row['perm']),
                    email=str(row['email']),
                    comments=str(row['comments']),
                    source_type=None if row['source_type'] is None else str(row['source_type']),
                    source_notes=None if row['source_notes'] is None else str(row['source_notes']),
                    parent_id=parent_id_data,
                    filters=filter_data
                ))

            if len(data) == 0:
                optional_message = " matching cohort id " + str(cohort_id) if cohort_id is not None else ""
                raise endpoints.NotFoundException("{} has no active cohorts{}."
                                                  .format(user_email, optional_message))
            return CohortDetailsList(items=data, count=len(data))

        except (IndexError, TypeError) as e:
            raise endpoints.NotFoundException(
                "User {}'s cohorts not found. {}: {}".format(user_email, type(e), e))

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

    POST_RESOURCE = endpoints.ResourceContainer(MetadataRangesItem)
    @endpoints.method(POST_RESOURCE, CohortPatientsSamplesList)
    def preview(self, request):
        """
        Takes a JSON object of filters in the request body and returns a "preview" of the cohort that would
        result from passing a similar request to the cohort **save** endpoint.  This preview consists of
        two lists: the lists of participant (aka patient) barcodes, and the list of sample barcodes.
        Authentication is not required.
        """
        patient_cursor = None
        sample_cursor = None
        db = None

        if are_there_bad_keys(request) or are_there_no_acceptable_keys(request):
            err_msg = construct_parameter_error_message(request, True)
            raise endpoints.BadRequestException(err_msg)

        query_dict = {
            k.name: request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and not k.name.endswith('_gte') and not k.name.endswith('_lte')
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
                    patient_query_str += ' OR {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
                    sample_query_str += ' OR {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
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
            raise endpoints.NotFoundException("Error retrieving samples or patients: {}".format(e))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\tpatient query: {} {}\n\tsample query: {} {}' \
                .format(e, patient_query_str, value_tuple, sample_query_str, value_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error previewing cohort. {}".format(msg))
        finally:
            if patient_cursor: patient_cursor.close()
            if sample_cursor: sample_cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)

        return CohortPatientsSamplesList(patients=patient_barcodes,
                                         patient_count=len(patient_barcodes),
                                         samples=sample_barcodes,
                                         sample_count=len(sample_barcodes))