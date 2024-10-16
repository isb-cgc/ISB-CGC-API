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
from cohorts_views import get_cohort_info, get_cohorts, get_file_manifest, get_cohort_counts, create_cohort, edit_cohort
from auth import auth_info, UserValidationException, validate_user
from django.conf import settings
from django.db import close_old_connections
from api_logging import *

logger = logging.getLogger(__name__)


@app.route('/v4/cohorts/<int:cohort_id>/', methods=['GET', 'PATCH', 'DELETE'], strict_slashes=False)
def cohort(cohort_id):
    """
    GET: Retrieve extended information for a specific cohort
    PATCH: Edit an extent cohort
    """

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'], cohort_id)

        code = None
        response_obj = None

        if not user:
            raise Exception('Encountered an error while attempting to identify this user.')
        else:
            if cohort_id <= 0:
                logger.warning("[WARNING] Invalid cohort ID {}".format(str(cohort_id)))
                code = 400
                response_obj = {
                    'message': '"{}" is not a valid cohort ID.'.format(str(cohort_id))
                }
            else:
                st_logger.write_text_log_entry(log_name, user_activity_message.format(user_info['email'], request.method, request.full_path))
                if request.method == 'GET':
                    include_barcodes = (request.args.get('include_barcodes', default="false", type=str).lower() == "true")
                    cohort_info = get_cohort_info(cohort_id, include_barcodes)
                else:
                    cohort_info = edit_cohort(cohort_id, user, delete=(request.method == 'DELETE'))

                if cohort_info:
                    response_obj = {'data': cohort_info}
                    code = 200
                    if 'message' in cohort_info:
                        code = 400
                        if not cohort_info.get('delete_permission',False):
                            code = 403
                else:
                    response_obj = {
                        'message': "Cohort ID {} was not found.".format(str(cohort_id))
                    }
                    code = 404

    except UserValidationException as e:
        response_obj = {
            'message': str(e)
        }
        code = 403
    except Exception as e:
        logger.exception(e)
        response_obj = {
            'message': 'Encountered an error while attempting to retrieve this cohort\'s information.'
        }
        code = 500
    finally:
        close_old_connections()

    response_obj['code'] = code
    response = jsonify(response_obj)
    response.status_code = code

    return response


@app.route('/v4/cohorts/', methods=['GET', 'POST'], strict_slashes=False)
def cohorts():
    """
    GET: Retrieve a user's list of cohorts
    POST: Add a new cohort
    """
    
    response_obj = None
    info = None
    code = None

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'])

        if not user:
            raise Exception('Encountered an error while attempting to identify this user.')
        else:
            st_logger.write_text_log_entry(log_name, user_activity_message.format(user_info['email'], request.method, request.full_path))
            info = get_cohorts(user_info['email']) if request.method == 'GET' else create_cohort(user)

            if info:
                response_obj = {
                    'data': info
                }

                code = 400 if 'message' in info else 200

            # Lack of a valid object means something went wrong on the server
            else:
                raise Exception("Invalid response while attempting to {}.".format(
                    'retrieve the cohort list' if request.method == 'GET' else 'create this cohort'
                ))

    except UserValidationException as e:
        response_obj = {
            'message': str(e)
        }
        code = 403
    except Exception as e:
        logger.exception(e)
        response_obj = {
            'message': 'Encountered an error while attempting to {}.'.format(
                "retrieve a list of cohorts" if request.method == 'GET' else "create this cohort"
            )
        }
        code = 500
    finally:
        close_old_connections()

    response_obj['code'] = code
    response = jsonify(response_obj)
    response.status_code = code
        
    return response


@app.route('/v4/cohorts/<int:cohort_id>/file_manifest/', methods=['POST', 'GET'], strict_slashes=False)
def cohort_file_manifest(cohort_id):
    """
    GET: Retrieve a cohort's file manifest
    POST: Retrieve a cohort's file manifest with applied filters
    """

    response_obj = None
    code = None

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'], cohort_id)

        if not user:
            raise Exception('Encountered an error while attempting to identify this user.')
        else:
            if cohort_id <= 0:
                logger.warning("[WARNING] Invalid cohort ID {}".format(str(cohort_id)))
                code = 400
                response_obj = {
                    'message': '"{}" is not a valid cohort ID.'.format(str(cohort_id))
                }
            else:
                st_logger.write_text_log_entry(log_name, user_activity_message.format(user_info['email'], request.method, request.full_path))
                file_manifest = get_file_manifest(cohort_id, user)
                if file_manifest:
                    # Presence of a message means something went wrong with our request
                    if 'message' in file_manifest:
                        response_obj = file_manifest
                        code = 400
                    else:
                        code = 200
                        response_obj = {
                            'data': file_manifest
                        }
                else:
                    raise Exception("Invalid response while attempting to retrieve file manifest for cohort {}.".format(str(cohort_id)))

    except UserValidationException as e:
        response_obj = {
            'message': str(e)
        }
        code = 403
    except Exception as e:
        logger.exception(e)
        response_obj = {
            'message': 'Encountered an error while attempting to identify this user.'
        }
        code = 500
    finally:
        close_old_connections()

    response_obj['code'] = code
    response = jsonify(response_obj)
    response.status_code = code
        
    return response


@app.route('/v4/cohorts/preview/', methods=['POST'], strict_slashes=False)
def cohort_preview():
    """List the samples, cases, and counts a given set of cohort filters would produce"""

    code = None
    response_obj = None

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))

    try:
        cohort_counts = get_cohort_counts()
        
        if cohort_counts:
            # Presence of a message means something went wrong with the filters we received
            if 'message' in cohort_counts:
                response_obj = cohort_counts
                code = 400
            else:
                response_obj = {
                    'data': cohort_counts
                }
                code = 200
                
        # Lack of a valid object means something went wrong on the server
        else:
            raise Exception("Invalid response while attempting to retrieve case and sample counts for these filters.")

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
