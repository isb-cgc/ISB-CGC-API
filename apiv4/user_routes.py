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
from flask import jsonify, request
from apiv4 import app
from auth import auth_info, UserValidationException, validate_user, get_user
from user_views import get_user_acls, get_account_details, gcp_validation, gcp_registration
from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/apiv4/users/account_details/', methods=['GET'], strict_slashes=False)
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
                response.status_code = 200
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

    return response


@app.route('/apiv4/users/gcp/validate/<gcp_id>/', methods=['GET'], strict_slashes=False)
def validate_gcp(gcp_id):
    """
    GET: Validate a Google Cloud Project for registration and return the results to the user
    """

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'])

        response = None

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            validation = gcp_validation(user, gcp_id)

            if validation:
                response_obj = {}
                code = None

                if 'message' in validation:
                    response_obj['message'] = validation['message']
                if 'notes' in validation:
                    response_obj['notes'] = validation['notes']

                if 'roles' not in validation:
                    code = 400
                else:
                    code = 200
                    response_obj['gcp_project_id'] = validation['gcp_id']

                response_obj['code'] = code
                response = jsonify(response_obj)
                response.status_code = code

            # Lack of a valid object means something went wrong on the server
            else:
                response = jsonify({
                    'code': 500,
                    'message': "Encountered an error while attempting to validate Google Cloud Platform project ID {}.".format(gcp_id)
                })
                response.status_code = 500

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
            'message': 'Encountered an error while attempting to validate Google Cloud Platform project ID {}.'.format(gcp_id)
        })
        response.status_code = 500

    return response


@app.route('/apiv4/users/gcp/register/<gcp_id>/', methods=['POST'], strict_slashes=False)
def register_gcp(gcp_id):
    """
    POST: Register a Google Cloud Project with ISB-CGC
    """

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'])

        response = None

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            request_data = request.get_json()
            
            registration, success = gcp_registration(user, gcp_id, False)

            if registration:
                response_obj = {}
                code = None

                if 'message' in validation:
                    response_obj['message'] = validation['message']
                if 'notes' in validation:
                    response_obj['notes'] = validation['notes']

                if not success:
                    code = 400
                else:
                    code = 200
                    response_obj['gcp_project_id'] = validation['gcp_id']

                response_obj['code'] = code
                response = jsonify(response_obj)
                response.status_code = code
                    
            # Lack of a valid object means something went wrong on the server
            else:
                response = jsonify({
                    'code': 500,
                    'message': "Encountered an error while attempting to register Google Cloud Platform project ID {}.".format(gcp_id)
                })
                response.status_code = 500

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
            'message': 'Encountered an error while attempting to register Google Cloud Platform project ID {}.'.format(
                gcp_id)
        })
        response.status_code = 500

    return response


@app.route('/apiv4/users/gcp/refresh/<gcp_id>/', methods=['PATCH'], strict_slashes=False)
def refresh_gcp(gcp_id):
    """
    PATCH: Refresh a Google Cloud Project with ISB-CGC, updating its user list
    """

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'])

        response = None

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            refresh, success = gcp_registration(user, gcp_id, True)

            if refresh:
                response_obj = {}
                code = None

                if 'message' in validation:
                    response_obj['message'] = validation['message']
                if 'notes' in validation:
                    response_obj['notes'] = validation['notes']

                if not success:
                    code = 400
                else:
                    code = 200
                    response_obj['gcp_project_id'] = validation['gcp_id']

                response_obj['code'] = code
                response = jsonify(response_obj)
                response.status_code = code

            # Lack of a valid object means something went wrong on the server
            else:
                response = jsonify({
                    'code': 500,
                    'message': "Encountered an error while attempting to refresh Google Cloud Platform project ID {}.".format(
                        gcp_id)
                })
                response.status_code = 500

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
            'message': 'Encountered an error while attempting to refresh Google Cloud Platform project ID {}.'.format(
                gcp_id)
        })
        response.status_code = 500

    return response
