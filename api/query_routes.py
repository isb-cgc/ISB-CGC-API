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
from . query_views import post_query_preview, post_query, get_query_next_page

from . auth import auth_info, UserValidationException
from python_settings import settings

logger = logging.getLogger(settings.LOGGER_NAME)

from flask import Blueprint

cohort_query_bp = Blueprint('query_bp', __name__, url_prefix='/{}'.format(settings.API_VERSION))

@cohort_query_bp.route('/cohorts/query/<int:cohort_id>', methods=['POST'], strict_slashes=False)
def cohorts_query(cohort_id):
    try:
        user_info = auth_info()
        if not user_info:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            result = post_query(user_info["email"], cohort_id)
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
                    'message': "Error trying to get metadata."})
                response.status_code = 500

    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to get metadata.'
        })
        response.status_code = 500

    return response


@cohort_query_bp.route('/cohorts/query/preview', methods=['POST'], strict_slashes=False)
def cohorts_preview_query():
    try:
        user_info = auth_info()
        result = post_query_preview(user_info['email'])
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
                'message': "Error trying to get metadata."})
            response.status_code = 500

    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to get metadata.'
        })
        response.status_code = 500

    return response


@cohort_query_bp.route('/cohorts/query/nextPage', methods=['GET'], strict_slashes=False)
def cohorts_query_next_page():
    try:
        user_info = auth_info()
        result = get_query_next_page(user_info['email'])
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
                'message': "Error trying to get next query page."})
            response.status_code = 500

    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to get next query page.'
        })
        response.status_code = 500

    return response
