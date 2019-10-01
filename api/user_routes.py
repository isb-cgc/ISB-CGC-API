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
from flask import jsonify, request
from api import app
from auth import auth_info, UserValidationException, get_user
from user_views import get_account_details
from django.conf import settings
from django.db import close_old_connections

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/v1/users/account_details/', methods=['GET'], strict_slashes=False)
def account_details():
    """
    GET: Retrieve extended information for a specific user
    """

    try:
        user_info = auth_info()
        user = get_user(user_info['email'])

        response = None

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:

            account_info = get_account_details(user)             

            if account_info:
                response_obj = {}
                code = None

                if 'message' in account_info:
                    code = 400
                else:
                    code = 200
                response_obj['data'] = account_info
                response_obj['code'] = code
                response = jsonify(response_obj)
                response.status_code = code
            else:
                response = jsonify({
                    'code': 404,
                    'message': "Unable to retrieve information for {}.".format(str(user_info['email']))})
                response.status_code = 404

    except UserValidationException as e:
        response = jsonify({
            'code': 403,
            'message': str(e)
        })
        response.status_code = 403
    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to retrieve user information.'
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response
