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
from apiv4 import app
from auth import auth_info, UserValidationException, validate_user, get_user
from user_views import get_user_acls, get_account_details, gcp_validation, gcp_registration, gcp_info
from django.conf import settings
from django.db import close_old_connections

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/v4/users/account_details/', methods=['GET'], strict_slashes=False)
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


@app.route('/v4/users/gcp/validate/<gcp_id>/', methods=['GET'], strict_slashes=False)
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
    finally:
        close_old_connections()
        
    return response


@app.route('/v4/users/gcp/<gcp_id>/', methods=['POST', 'DELETE', 'PATCH', 'GET'], strict_slashes=False)
def user_gcp(gcp_id):
    """
    POST: Register a Google Cloud Project with ISB-CGC
    PATCH: Update the Google Cloud Project's user list with ISB-CGC
    DELETE: Unregister the Google Cloud Project with ISB-CGC
    GET: Fetch details about the Google Cloud Project
    """

    response_obj = {}
    code = None
    
    try:
        user_info = auth_info()
        user = validate_user(user_info['email'])

        if not user:
            response_obj = {
                'message': 'Encountered an error while attempting to identify this user.'
            }
            code = 500
        else:
            action = None
            result = None
            success = False
            
            if request.method == 'POST' or request.method == 'PATCH':
                action, success = gcp_registration(user, gcp_id, False)
            elif request.method == 'GET':
                result, success = gcp_info(user, gcp_id)
            elif request.method == 'DELETE':
                action, success = gcp_unregistration(user, gcp_id, False)
            else:
                raise Exception("Method not recognized: {}".format(request.method))

            if not success:
                if result is not None:
                    code = 404
                    response_obj['message'] = 'A Google Cloud Platform project with ID {} was not found for user {}'.format(
                        gcp_id, user.email
                    )
            else:
                code = 200
    
            if action is not None:
                if 'message' in action:
                    response_obj['message'] = action['message']
                if 'notes' in action:
                    response_obj['notes'] = action['notes']
                if success:
                    response_obj['gcp_project_id'] = action['gcp_id']
            elif result is not None:
                if len(result):
                    response_obj['data'] = result
    
            # Lack of a valid object means something went wrong on the server
            else:
                code = 500
                act = "fetch"
                if request.method == 'POST':
                    act = "register"
                if request.method == 'DELETE':
                    act = "unregister"
                if request.method == "PATCH":
                    act = "refresh"
                response_obj = {
                    'message': "Encountered an error while attempting to {} Google Cloud Platform project ID {}.".format(
                        act,
                        gcp_id
                    )
                }

    except UserValidationException as e:
        code = 403
        response_obj = {
            'message': str(e)
        }

    except Exception as e:
        logger.error("[ERROR] For route /v4/users/gcp/{gcp_id} method {}:".format(request.method))
        logger.exception(e)
        code = 500
        response_obj = {
            'message': 'Encountered an error while attempting to register Google Cloud Platform project ID {}.'.format(
                gcp_id)
        }
    finally:
        close_old_connections()
        
    response_obj['code'] = code
    response = jsonify(response_obj)
    response.status_code = code

    return response

@app.route('/v4/users/gcp/', methods=['POST', 'GET'], strict_slashes=False)
def user_gcps():
    """
    POST: Register a Google Cloud Project with ISB-CGC
    PATCH: Update the Google Cloud Project's user list with ISB-CGC
    DELETE: Unregister the Google Cloud Project with ISB-CGC
    GET: Fetch details about the Google Cloud Project
    """

    response_obj = {}
    code = None
    gcp_id = None

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'])

        if not user:
            response_obj = {
                'message': 'Encountered an error while attempting to identify this user.'
            }
            code = 500
        else:
            action = None
            result = None
            success = None

            if request.method == 'POST':
                gcp_id = request.args.get('project_id', default=None, type=string)
                if gcp_id:
                    action, success = gcp_registration(user, gcp_id, False)
            elif request.method == 'GET':
                result, success = gcp_info(user)
            else:
                raise Exception("Method not recognized: {}".format(request.method))

            if not success:
                if result is not None:
                    code = 404
                    response_obj['message'] = 'No Google Cloud Platform projects found for user {}'.format(
                        gcp_id, user.email
                    )
            else:
                code = 200

            if action:
                if 'message' in action:
                    response_obj['message'] = action['message']
                if 'notes' in action:
                    response_obj['notes'] = action['notes']
                if success:
                    response_obj['gcp_project_id'] = action['gcp_id']
            elif result:
                response_obj['data'] = result

            # Lack of a valid object means something went wrong on the server
            else:
                code = 500
                act = "fetch the registered GCP project list for user {}".format(user.email)
                if request.method == 'POST':
                    if gcp_id:
                        act = "register Google Cloud Platform project ID {}".format(gcp_id)
                    else:
                        act = "register a Google Cloud Platform project"
                response_obj = {
                    'message': "Encountered an error while attempting to {}".format(
                        act
                    )
                }

    except UserValidationException as e:
        code = 403
        response_obj = {
            'message': str(e)
        }

    except Exception as e:
        logger.error("[ERROR] For route /v4/users/gcp/{gcp_id} method {}:".format(request.method))
        logger.exception(e)
        code = 500
        response_obj = {
            'message': 'Encountered an error while attempting to register Google Cloud Platform project ID {}.'.format(
                gcp_id)
        }
    finally:
        close_old_connections()

    response_obj['code'] = code
    response = jsonify(response_obj)
    response.status_code = code

    return response





