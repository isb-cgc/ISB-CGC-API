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
from flask import jsonify, request
from . cohorts_views import create_cohort, get_cohort_objects, get_cohort_manifest, get_cohort_list, delete_cohort, \
    delete_cohorts, post_cohort_preview, get_cohort_preview_manifest  # get_file_manifest
from . auth import auth_info, UserValidationException
from python_settings import settings

logger = logging.getLogger(settings.LOGGER_NAME)

from flask import Blueprint

cohorts_bp = Blueprint('cohorts_bp', __name__, url_prefix='/v1')


@cohorts_bp.route('/cohorts/<int:cohort_id>/manifest/', methods=['GET'], strict_slashes=False)
def cohort_manifest(cohort_id):
    """
    GET: Retrieve extended information for a specific cohort
    DELETE: Delete a cohort
    """
    try:
        user_info = auth_info()
        if not user_info:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            result = get_cohort_manifest(user_info["email"], cohort_id)
            if result:
                if 'message' in result:
                    response = jsonify({
                        **result
                    })
                    if 'code' in result:
                        response.status_code = result['code']
                    else:
                        response.status_code = 500
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
                response.status_code = 500

    except UserValidationException as e:
        response = jsonify({
            'code': 403,
            'message': str(e)
        })
        response.status_code = 500
    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to retrieve this cohort\'s information.'
        })
        response.status_code = 500

    return response


@cohorts_bp.route('/cohorts/<int:cohort_id>/', methods=['GET', 'DELETE'], strict_slashes=False)
def cohort(cohort_id):
    """
    GET: Retrieve extended information for a specific cohort
    DELETE: Delete a cohort
    """
    try:
        user_info = auth_info()
        if not user_info:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            if request.method == 'GET':
                result = get_cohort_objects(user_info["email"], cohort_id)
                if result:
                    if 'message' in result:
                        response = jsonify({
                            **result
                        })
                        response.status_code = 500
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
                    response.status_code = 500
            else:
                results = delete_cohort(user_info["email"], cohort_id)

                if results:
                    if 'message' in results:
                        response = jsonify({
                            **results
                        })
                        response.status_code = 500
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
        response.status_code = 500
    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to retrieve this cohort\'s information.'
        })
        response.status_code = 500

    return response


@cohorts_bp.route('/cohorts/', methods=('GET', 'POST', 'DELETE'), strict_slashes=False)
def cohorts():
    """
    GET: Retrieve a user's list of cohorts
    POST: Add a new cohort
    DELETE: Delete a list of cohorts
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
            if request.method == 'GET':
                result = get_cohort_list(user_info["email"])
            elif request.method == 'POST':
                result = create_cohort(user_info["email"])
            else:
                result = delete_cohorts(user_info["email"])
            if result:
                if 'message' in result:
                    response = jsonify({
                        **result
                    })
                    if 'code' in result:
                        response.status_code = result['code']
                    else:
                        response.status_code = 500
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
        response.status_code = 500
    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to {}.'.format(
                "retrieve a list of cohorts" if request.method == 'GET' else "create this cohort"
            )
        })
        response.status_code = 500

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

    try:
        result = post_cohort_preview()

        if result:
            # Presence of a message means something went wrong with the filters we received
            if 'message' in result:
                response = jsonify({
                    **result
                })
                if 'code' in result:
                    response.status_code = result['code']
                else:
                    response.status_code = 500
            else:
                code = 200
                response = jsonify({
                    'code': code,
                    **result
                })
                response.status_code = code

        # Lack of a valid object means something went wrong on the server
        else:
            response = jsonify({
                'code': 404,
                'message': "Error trying to preview cohort."})
            response.status_code = 500

    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to retrieve this cohort\'s information.'
        })
        response.status_code = 500

    return response


@cohorts_bp.route('/cohorts/preview/manifest/', methods=['POST'], strict_slashes=False)
def cohort_preview_manifest():
    """
    GET: Retrieve manifest for a previewed cohort
    """
    try:
        result = get_cohort_preview_manifest()
        if result:
            if 'message' in result:
                response = jsonify({
                    **result
                })
                if 'code' in result:
                    response.status_code = result['code']
                else:
                    response.status_code = 500
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
            response.status_code = 500

    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to retrieve this cohort\'s information.'
        })
        response.status_code = 500

    return response
