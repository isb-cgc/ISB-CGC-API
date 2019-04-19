"""

Copyright 2019, Institute for Systems Biology

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

import logging
import json
import django
import re

from flask import request

from django.core.signals import request_finished
from django.contrib.auth.models import User as Django_User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings

from accounts.sa_utils import auth_dataset_whitelists_for_user
from accounts.utils import register_or_refresh_gcp, verify_gcp_for_reg
from accounts.sa_utils import auth_dataset_whitelists_for_user
from accounts.models import AuthorizedDataset
from projects.models import Program
from auth import get_user_acls, UserValidationException

from jsonschema import validate as schema_validate, ValidationError

BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(settings.LOGGER_NAME)


def get_account_details(user):
    accounts_details = None

    try:
        whitelists = get_user_acls(user)

        if whitelists:
            uads = AuthorizedDataset.objects.filter(whitelist_id__in=whitelists)
            accounts_details = {'dataset_access': [{'name': uad.name, 'whitelist_id': uad.whitelist_id} for uad in uads]}

    except UserValidationException as u:
        logger.warn(u)
        accounts_details = {'message': str(u)}

    except Exception as e:
        logger.error("[ERROR] Encountered an error while retrieving user account details:")
        logger.exception(e)
        accounts_details = {'message': "Encountered an error while retrieving account details for {}.".format(user.email)}

    return accounts_details


def gcp_validation(user, gcp_id):
    validation = None

    try:
        validation, status = verify_gcp_for_reg(user, gcp_id)

        if validation:
            if 'roles' in validation:
                unregs = [x for x in validation['roles'] if not validation['roles'][x]['registered']]

                if len(unregs):
                    validation['notes'] = "The following users are not registered in our system. Please note that if GCP {} ".format(gcp_id) + \
                       "is intended for use with controlled access data, all users must log in to the ISB-CGC " + \
                       "web application at <https://isb-cgc.appspot.com> and link their Google Account to their eRA " + \
                       "Commons ID. The link to do so is found in Account Settings. Unregistered users: " + \
                       "{}".format("; ".join(unregs))

                if 'message' not in validation:
                    validation['message'] = "Google Cloud Platform project ID {} was successfully validated for registration.".format(gcp_id)

    except Exception as e:
        logger.exception(e)

    return validation


def gcp_registration(user, gcp_id, refresh):

    registration = None
    success = False
    try:
        validation = verify_gcp_for_reg(user, gcp_id, refresh)

        if validation:
            if 'roles' in validation:

                registered_users = [x for x, y in validation['roles'].items() if y['registered_user']]

                registration, status = register_or_refresh_gcp(user, gcp_id, registered_users, refresh)

                if status == 200:
                    success = True
                    unregs = [x for x in validation['roles'] if not validation['roles'][x]['registered']]
                    if len(unregs):
                        registration['notes'] = "The following users are not registered in our system. Please note that if GCP {} ".format(gcp_id) + \
                           "is intended for use with controlled access data, all users must log in to the ISB-CGC " + \
                           "web application at <https://isb-cgc.appspot.com> and link their Google Account to their eRA " + \
                           "Commons ID. The link to do so is found in Account Settings. Unregistered users: " + \
                           "{}".format("; ".join(unregs))
                        
                    if 'message' not in registration:
                        registration['message'] = "Google Cloud Platform project ID {} was successfully {}.".format(gcp_id, 'refreshed' if refresh else 'registered')
    
    except Exception as e:
        logger.exception(e)

    return registration, success
