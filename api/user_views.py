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
import json
import requests

from flask import request
from werkzeug.exceptions import BadRequest

import datetime

from python_settings import settings
from . auth import UserValidationException, get_auth

logger = logging.getLogger(settings.LOGGER_NAME)

def get_account_details(user):
    account_details = None

    path_params = {'email': user}
    try:
        auth = get_auth()
        response = requests.get("{}/users/api/".format(settings.BASE_URL),
                                 params=path_params, headers=auth)
        account_details = response.json()

        account_details['user_details']['date_joined'] = datetime.datetime.fromtimestamp(
            int(account_details['user_details']['date_joined']))
        account_details['user_details']['last_login'] = datetime.datetime.fromtimestamp(
            int(account_details['user_details']['last_login']))
    except BadRequest as e:
        logger.warn("[WARNING] Received bad request - couldn't load JSON.")
        account_details = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
            'code': 400
        }

    except UserValidationException as u:
        logger.warning(u)
        account_details = {'message': str(u)}

    except Exception as e:
        logger.error("[ERROR] Encountered an error while retrieving user account details:")
        logger.exception(e)
        account_details = {'message': "Encountered an error while retrieving account details for {}.".format(user.email)}

    return account_details
