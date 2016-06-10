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
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from django.core.signals import request_finished
from protorpc import remote, messages

from cohort_helpers import Cohort_Endpoints2
from api.api_helpers import sql_connection, get_user_email_from_token

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class CohortPatientsSamplesListItem(messages.Message):
    patients = messages.StringField(1, repeated=True)
    patient_count = messages.IntegerField(2)
    samples = messages.StringField(3, repeated=True)
    sample_count = messages.IntegerField(4)
    cohort_id = messages.IntegerField(5)


@Cohort_Endpoints2.api_class(resource_name='cohort_patients_samples_list_endpoints')
class CohortsPatientsSamplesList(remote.Service):
    GET_RESOURCE = endpoints.ResourceContainer(token=messages.StringField(1), cohort_id=messages.IntegerField(2))

    @endpoints.method(GET_RESOURCE, CohortPatientsSamplesListItem,
                      path='cohort_patients_samples_list2', http_method='GET',
                      name='cohorts.cohort_patients_samples_list2')
    def cohort_patients_samples_list2(self, request):
        """
        Takes a cohort id as a required parameter and returns information about the participants
        and samples in a particular cohort. Authentication is required.
        User must have either READER or OWNER permissions on the cohort.
        """

        db = None
        cursor = None
        user_email = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        # users have the option of pasting the access token in the query string
        # or in the 'token' field in the api explorer
        # but this is not required
        access_token = request.get_assigned_value('token')
        if access_token:
            user_email = get_user_email_from_token(access_token)

        cohort_id = request.get_assigned_value('cohort_id')

        if user_email:
            django.setup()
            try:
                user_id = Django_User.objects.get(email=user_email).id
            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                request_finished.send(self)
                raise endpoints.UnauthorizedException(
                    "Authentication failed. Try signing in to {} to register with the web application."
                        .format(BASE_URL))

            cohort_perms_query = "select count(*) from cohorts_cohort_perms where user_id=%s and cohort_id=%s"
            cohort_perms_tuple = (user_id, cohort_id)
            cohort_query = "select count(*) from cohorts_cohort where id=%s and active=%s"
            cohort_tuple = (cohort_id, unicode('0'))

            try:
                db = sql_connection()
                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(cohort_perms_query, cohort_perms_tuple)
                result = cursor.fetchone()
                if int(result['count(*)']) == 0:
                    error_message = "{} does not have owner or reader permissions on cohort {}.".format(user_email,
                                                                                                        cohort_id)
                    request_finished.send(self)
                    raise endpoints.ForbiddenException(error_message)

                cursor.execute(cohort_query, cohort_tuple)
                result = cursor.fetchone()
                if int(result['count(*)']) > 0:
                    error_message = "Cohort {} was deleted.".format(cohort_id)
                    request_finished.send(self)
                    raise endpoints.NotFoundException(error_message)

            except (IndexError, TypeError) as e:
                logger.warn(e)
                raise endpoints.NotFoundException("Cohort {} not found.".format(cohort_id))
            except MySQLdb.ProgrammingError as e:
                msg = '{}:\n\tcohort permissions query: {} {}\n\tcohort query: {} {}' \
                    .format(e, cohort_perms_query, cohort_perms_tuple, cohort_query, cohort_tuple)
                logger.warn(msg)
                raise endpoints.BadRequestException("Error retrieving cohorts or cohort permissions. {}".format(msg))
            finally:
                if cursor: cursor.close()
                if db and db.open: db.close()
                request_finished.send(self)

            patient_query_str = 'select cohorts_patients.patient_id ' \
                                'from cohorts_patients ' \
                                'inner join cohorts_cohort_perms ' \
                                'on cohorts_cohort_perms.cohort_id=cohorts_patients.cohort_id ' \
                                'inner join cohorts_cohort ' \
                                'on cohorts_patients.cohort_id=cohorts_cohort.id ' \
                                'where cohorts_patients.cohort_id=%s ' \
                                'and cohorts_cohort_perms.user_id=%s ' \
                                'and cohorts_cohort.active=%s ' \
                                'group by cohorts_patients.patient_id '

            patient_query_tuple = (cohort_id, user_id, unicode('1'))

            sample_query_str = 'select cohorts_samples.sample_id ' \
                               'from cohorts_samples ' \
                               'inner join cohorts_cohort_perms ' \
                               'on cohorts_cohort_perms.cohort_id=cohorts_samples.cohort_id ' \
                               'inner join cohorts_cohort ' \
                               'on cohorts_samples.cohort_id=cohorts_cohort.id ' \
                               'where cohorts_samples.cohort_id=%s ' \
                               'and cohorts_cohort_perms.user_id=%s ' \
                               'and cohorts_cohort.active=%s ' \
                               'group by cohorts_samples.sample_id '

            sample_query_tuple = (cohort_id, user_id, unicode('1'))

            try:
                db = sql_connection()

                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(patient_query_str, patient_query_tuple)
                patient_data = []
                for row in cursor.fetchall():
                    patient_data.append(row['patient_id'])

                cursor.execute(sample_query_str, sample_query_tuple)
                sample_data = []
                for row in cursor.fetchall():
                    sample_data.append(row['sample_id'])

                return CohortPatientsSamplesList(patients=patient_data,
                                                 patient_count=len(patient_data),
                                                 samples=sample_data,
                                                 sample_count=len(sample_data),
                                                 cohort_id=int(cohort_id))
            except (IndexError, TypeError) as e:
                logger.warn(e)
                raise endpoints.NotFoundException("Cohort {} not found.".format(cohort_id))
            except MySQLdb.ProgrammingError as e:
                msg = '{}:\n\tpatient query: {} {}\n\tsample query: {} {}' \
                    .format(e, patient_query_str, patient_query_tuple, sample_query_str, sample_query_tuple)
                logger.warn(msg)
                raise endpoints.BadRequestException("Error retrieving patients or samples. {}".format(msg))
            finally:
                if cursor: cursor.close()
                if db and db.open: db.close()
                request_finished.send(self)

        else:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))