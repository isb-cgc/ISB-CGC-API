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
import os
from flask import request
from python_settings import settings

logger = logging.getLogger(settings.LOGGER_NAME)


class UserValidationException(Exception):
    pass

def get_auth():
    auth = {"X-API-AUTH": "APIToken {}".format(settings.API_AUTH_TOKEN)}
    return auth


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
    elif os.getenv("DEBUG"):
        logger.debug("[STATUS] Using debug API user info")
        user_info = {
            'id' : settings.DEBUG_API_ID,
            'email' : settings.DEBUG_API_EMAIL
            # 'id': os.getenv('DEBUG_API_ID'),
            # 'email': os.getenv('DEBUG_API_EMAIL')
        }
    else:
        logger.info("[STATUS] No user encoded info found.")
        user_info = {'id': 'anonymous', 'email': 'Anonymous'}

    return user_info


