# 
# Copyright 2019, Institute for Systems Biology
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import base64
import json
import requests
import django
from flask import request, jsonify
from django.conf import settings
from django.contrib.auth.models import User as Django_User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from cohorts.models import Cohort_Perms

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
        if 'email' not in user_info:
            raise UserValidationException("Couldn't obtain user email - the correct scopes may not have been provided during authorization!")
    else:
        logger.warning("[WARNING] No user encoded info found.")
        user_info = {'id': 'anonymous', 'email': 'Anonymous'}

    return user_info


def get_user(user_email=None):
    # Assume this is for the user information in the request header if none is
    # provided (it could be for someone else on a project, etc.)
    if not user_email:
        user_email = auth_info()['email']

    django.setup()
    try:
        user = Django_User.objects.get(email=user_email)
        logger.info("[USER API AUTH] User {} seen in API".format(user_email))
    except ObjectDoesNotExist as e:
        logger.warning("User {} does not exist in our system.".format(user_email))
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
        logger.warning("Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e))
        raise UserValidationException(
            "User {} does not have access to cohort {}.".format(user_email, cohort_id) +
            " Please contact this cohort owner to obtain permission."
        )

    return user


# END METHODS
