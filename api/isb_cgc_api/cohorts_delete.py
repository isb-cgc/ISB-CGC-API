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

from cohorts.models import Cohort as Django_Cohort, Cohort_Perms


logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class ReturnJSON(messages.Message):
    message = messages.StringField(1)


@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortsDeleteAPI(remote.Service):
    DELETE_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True),
                                                  token=messages.StringField(2))

    @endpoints.method(DELETE_RESOURCE, ReturnJSON, http_method='DELETE', path='cohorts/{cohort_id}')
    def delete(self, request):
        """
        Deletes a cohort. User must have owner permissions on the cohort.
        """
        user_email = None
        return_message = None

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
                django_user = Django_User.objects.get(email=user_email)
                user_id = django_user.id
            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                request_finished.send(self)
                raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)
            try:
                cohort_to_deactivate = Django_Cohort.objects.get(id=cohort_id)
                if cohort_to_deactivate.active is True:
                    cohort_perm = Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user_id)
                    if cohort_perm.perm == 'OWNER':
                        cohort_to_deactivate.active = False
                        cohort_to_deactivate.save()
                        return_message = 'Cohort %d successfully deactivated.' % cohort_id
                    else:
                        return_message = 'You do not have owner permission on cohort %d.' % cohort_id
                else:
                    return_message = "Cohort %d was already deactivated." % cohort_id

            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                raise endpoints.NotFoundException(
                    "Either cohort %d does not have an entry in the database "
                    "or you do not have owner or reader permissions on this cohort." % cohort_id)
            finally:
                request_finished.send(self)
        else:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

        return ReturnJSON(message=return_message)
