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
#from api import app
from . cohorts_views import post_cohort_preview, create_cohort, get_cohort_objects, get_cohort_list, delete_cohort, delete_cohorts #, get_cohorts, get_file_manifest, get_cohort_preview, create_cohort, edit_cohort
from . auth import auth_info, UserValidationException, validate_user
from django.conf import settings
from django.db import close_old_connections

logger = logging.getLogger(settings.LOGGER_NAME)

from flask import Blueprint
from flask import g

cohorts_bp = Blueprint('cohorts_bp', __name__, url_prefix='/v1')


@cohorts_bp.route('/cohorts/<int:cohort_id>/', methods=['GET', 'DELETE'], strict_slashes=False)
def cohort(cohort_id):
    """
    GET: Retrieve extended information for a specific cohort
    """


    try:
        user_info = auth_info()
#        user = validate_user(user_info['email'], cohort_id)
        user = True

        response = None
        code = None

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            if request.method == 'GET':
                result = get_cohort_objects(cohort_id)
                if result:
                    if 'message' in result:
                        code = 400
                    else:
                        code = 200
                    response = jsonify({
                        'code': code,
                        **result
                    })
                    response.status_code = code

                else:
                    response = jsonify({
                        'code': 404,
                        'message': "Cohort ID {} was not found.".format(str(cohort_id))})
                    response.status_code = 404

            else:
                results = delete_cohort(cohort_id)

                if results:
                    if 'message' in results:
                        code = 400
                    else:
                        code = 200
                    response = jsonify({
                        'code': code,
                        **results
                    })
                    response.status_code = code

                else:
                    response = jsonify({
                        'code': 500,
                        'message': "Error while attempting to retrieve the cohort info"
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
            'message': 'Encountered an error while attempting to retrieve this cohort\'s information.'
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response




@cohorts_bp.route('/cohorts/', methods=('GET', 'POST', 'DELETE'), strict_slashes=False)
def cohorts():
    """
    GET: Retrieve a user's list of cohorts
    POST: Add a new cohort
    """
    
    response = None
    info = None
    code = None

    try:
        user_info = auth_info()
        #user = validate_user(user_info['email'])
        user = True

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            if request.method == 'GET':
                result = get_cohort_list(user)
            elif request.method == 'POST':
                result = create_cohort(user)
            else:
                result = delete_cohorts()
            if result:
                if 'message' in result:
                    code = 400
                else:
                    code = 200
                response = jsonify({
                    'code': code,
                    **result
                })
                response.status_code = code
            else:
                response = jsonify({
                    'code': 500,
                    'message': "Error while attempting to {}.".format(
                        'retrieve the cohort list' if request.method == 'GET' else 'create this cohort'
                    )
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
            'message': 'Encountered an error while attempting to {}.'.format(
                "retrieve a list of cohorts" if request.method == 'GET' else "create this cohort"
            )
        })
        response.status_code = 500
    finally:
        close_old_connections()
        
    return response

# @cohorts_bp.route('/manifest/<int:cohort_id>/', methods=['POST', 'GET'], strict_slashes=False)
# def cohort_file_manifest(cohort_id):
#     """
#     GET: Retrieve a cohort's file manifest
#     POST: Retrieve a cohort's file manifest with applied filters
#     """
#
#     response_obj = None
#     code = None
#
#     try:
#         user_info = auth_info()
#         user = validate_user(user_info['email'], cohort_id)
#
#         if not user:
#             response_obj = {
#                 'message': 'Encountered an error while attempting to identify this user.'
#             }
#             code = 500
#         else:
#             file_manifest = get_file_manifest(cohort_id, user)
#             if file_manifest:
#                 # Presence of a message means something went wrong with our request
#                 if 'message' in file_manifest:
#                     response_obj = file_manifest
#                     code = 400
#                 else:
#                     code = 200
#                     response_obj = {
#                         'data': file_manifest
#                     }
#             else:
#                 response_obj = {
#                     'message': "Error while attempting to retrieve file manifest for cohort {}.".format(str(cohort_id))
#                 }
#                 code = 500
#
#     except UserValidationException as e:
#         response_obj = {
#             'message': str(e)
#         }
#         code = 403
#     except Exception as e:
#         logger.exception(e)
#         response_obj = {
#             'message': 'Encountered an error while attempting to identify this user.'
#         }
#         code = 500
#     finally:
#         close_old_connections()
#
#     response_obj['code'] = code
#     response = jsonify(response_obj)
#     response.status_code = code
#
#     return response


@cohorts_bp.route('/cohorts/preview/', methods=['POST'], strict_slashes=False)
def cohort_preview():
    """List the samples, cases, and counts a given set of cohort filters would produce"""

    code = None
    response_obj = None

    try:
        cohort = post_cohort_preview()

        if cohort:
            # Presence of a message means something went wrong with the filters we received
            if 'message' in cohort:
                response_obj = cohort
                code = 400
            else:
                response_obj = {
                    'data': cohort
                }
                code = 200

        # Lack of a valid object means something went wrong on the server
        else:
            response_obj = {
                'message': "Error while attempting to retrieve case and sample counts for these filters."
            }
            code = 500

    except Exception as e:
        logger.exception(e)
        response_obj = {
            'message': 'Encountered an error while attempting to build this cohort preview.'
        }
        code = 500
    finally:
        close_old_connections()

    response_obj['code'] = code
    response = jsonify(response_obj)
    response.status_code = code

    return response




