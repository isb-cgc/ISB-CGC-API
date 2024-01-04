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
from .auth import auth_info, UserValidationException
from .user_views import get_account_details
from python_settings import settings
from .version_config import API_VERSION
from flask import Blueprint

logger = logging.getLogger(settings.LOGGER_NAME)

user_bp = Blueprint(f'user_bp_{API_VERSION}', __name__, url_prefix='/{}'.format(API_VERSION))

@user_bp.route('/users/account_details/', methods=['GET'], strict_slashes=False)
def account_details():
    """
    GET: Retrieve extended information for a specific user
    """

    try:
        user_info = auth_info()
        if not user_info:
            response = jsonify({
                'code': 403,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            results = get_account_details(user_info["email"])
            if 'message' in results:
                response = jsonify(results)
                response.status_code = results['code']
            else:
                response = jsonify({
                    'code': 200,
                    **results
                })
                response.status_code = 200


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

    return response