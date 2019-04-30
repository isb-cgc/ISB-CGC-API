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
import base64
import json
import requests
import django
from flask import request, jsonify
from django.conf import settings
# from cohorts.metadata_helpers import get_acls_by_uuid
from django.contrib.auth.models import User as Django_User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from cohorts.models import Cohort_Perms
from accounts.sa_utils import auth_dataset_whitelists_for_user
# from accounts.dcf_support import refresh_at_dcf, TokenFailure, InternalTokenError, DCFCommFailure, RefreshTokenExpired

logger = logging.getLogger(settings.LOGGER_NAME)


class UserValidationException(Exception):
    pass


# BEGIN METHODS
def _base64_decode(encoded_str):
    # Add paddings manually if necessary.
    num_missed_paddings = 4 - len(encoded_str) % 4
    if num_missed_paddings != 4:
        encoded_str += b'=' * num_missed_paddings
    return base64.b64decode(encoded_str).decode('utf-8')


def auth_info():
    """Retrieves the authenication information from Google Cloud Endpoints."""
    encoded_info = request.headers.get('X-Endpoint-API-UserInfo', None)

    if encoded_info:
        info_json = _base64_decode(encoded_info)
        user_info = json.loads(info_json)
    else:
        logger.info("[STATUS] No user encoded info found.")
        user_info = {'id': 'anonymous', 'email': 'Anonymous'}

    return user_info


def get_user(user_email=None):
    # Assume this is for the user information in the request header if none is
    # provided (it could be for someone else on a project, etc.)
    if not user_email:
        user_email = auth_info()['email']

    user = None

    django.setup()
    try:
        user = Django_User.objects.get(email=user_email)
    except ObjectDoesNotExist as e:
        logger.warn("User {} does not exist in our system.".format(user_email))
        raise UserValidationException(
            "User {} wasn't found in our system.".format(user_email) +
            " Please register with our Web Application first: <https://isb-cgc.appspot.com>"
        )
    
    return user


def validate_user(user_email=None, cohort_id=None, uuids=None):
    user = get_user()

    if not user_email:
        user_email = user.email

    try:
        if cohort_id:
            Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user.id)
    except ObjectDoesNotExist as e:
        logger.warn("Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e))
        raise UserValidationException(
            "User {} does not have access to cohort {}.".format(user_email, cohort_id) +
            " Please contact this cohort owner to obtain permission."
        )

    # if uuids:
    #     acls_needed = get_acls_by_uuid(uuids)
    #     user_acls = get_user_acls(user)
    # 
    #     logger.info("User ACLs: {}".format(str(user_acls)))
    #     logger.info("ACLs needed: {}".format(str(acls_needed)))
    #     inaccessible = []
    # 
    #     for acl in acls_needed:
    #         if acl not in user_acls:
    #             inaccessible.append(acl)
    #     
    #     if len(inaccessible):
    #         logger.warn(
    #             "User {} does not have access to one or more programs in this barcode set.".format(user_email))
    #         raise UserValidationException(
    #             "User {} does not have access to one or more programs in this barcode set.".format(user_email) +
    #             " Please double-check that you have linked the email '{}' to your eRA Commons ID via DCF and are currently signed in."
    #         )

    return user


def get_user_acls(user):
    user_acls = auth_dataset_whitelists_for_user(user.id)

    if not user_acls:
        raise UserValidationException("Couldn't verify user controlled data access for user {}.".format(user.email) + 
            " Please visit the web application at <https://isb-cgc.appspot.com> and attempt a login to DCF from" +
            " your Account Settings page, then verify your controlled dataset access."
        )
        
        
        # try:
        #     err_msg, expr_str, _ = refresh_at_dcf(user.id)
        #     exception_msg = None
        #     if err_msg:
        #         logger.warn(err_msg)
        #         exception_msg = "User {} not currently logged in via DCF and failed to refresh.".format(user.email) + \
        #             " Please visit the web application at <https://isb-cgc.appspot.com> and attempt a login to DCF from" + \
        #             " your Account Settings page."
        #     else:
        #         user_acls = auth_dataset_whitelists_for_user(user.id)
        # 
        #         if not user_acls:
        #             exception_msg = "Couldn't verify user controlled data access for user {}.".format(user.email) + \
        #                 " Please visit the web application at <https://isb-cgc.appspot.com> and attempt a login to DCF from" + \
        #                 " your Account Settings page, then verify your controlled dataset access."
        # 
        #     if exception_msg:
        #         raise UserValidationException(exception_msg)
        # 
        # except (TokenFailure, InternalTokenError, DCFCommFailure, RefreshTokenExpired) as e:
        #     if type(e) is RefreshTokenExpired:
        #         raise UserValidationException(
        #             "Unable to refresh your 24 hour access to controlled data. Please log in to Web "
        #             + "Application at <https://isb-cgc.appspot.com> and visit your Account Details page to refresh "
        #             + "your controlled dataset access.")
        #     else:
        #         if type(e) is DCFCommFailure:
        #             msg = "Unable to communicate with DCF while attempting to refresh user access for {}.".format(user.email)
        #         else:
        #             msg = "There is an internal inconsistency with user tokens for user {}".format(user.email)
        #         raise Exception(msg)

    return user_acls

# END METHODS
