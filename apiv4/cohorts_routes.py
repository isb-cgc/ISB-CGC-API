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
from cohorts_views import get_cohort_info, get_cohorts, get_file_manifest, get_cohort_counts, create_cohort, edit_cohort
from auth import auth_info, UserValidationException, validate_user
from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/apiv4/cohorts/<int:cohort_id>/', methods=['GET', 'PATCH', 'DELETE'], strict_slashes=False)
def cohort(cohort_id):
    """
    GET: Retrieve extended information for a specific cohort
    PATCH: Edit an extent cohort
    """

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'], cohort_id)

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
                include_barcodes = (request.args.get('include_barcodes', default="false", type=str).lower() == "true")
                cohort_info = get_cohort_info(cohort_id, include_barcodes)
            else:
                cohort_info = edit_cohort(cohort_id, delete=(request.method == 'DELETE)'))

            if cohort_info:
                response_obj = {}

                if 'message' in cohort_info:
                    code = 400
                else:
                    code = 200
                    
                response_obj['data'] = cohort_info
                response_obj['code'] = code
                response = jsonify(response_obj)
                response.status_code = code
                
            else:
                response = jsonify({
                    'code': 404,
                    'message': "Cohort ID {} was not found.".format(str(cohort_id))})
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
            'message': 'Encountered an error while attempting to retrieve this cohort\'s information.'
        })
        response.status_code = 500

    return response


@app.route('/apiv4/cohorts/', methods=['GET', 'POST'], strict_slashes=False)
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
        user = validate_user(user_info['email'])

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            if request.method == 'GET':
                info = get_cohorts(user_info['email'])
            else:
                info = create_cohort(user)

            if info:
                response_obj = {}
                
                if 'message' in info:
                    code = 400
                else:
                    code = 200

                response_obj['data'] = info
                response_obj['code'] = code
                response = jsonify(response_obj)
                response.status_code = code

            # Lack of a valid object means something went wrong on the server
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

    return response


@app.route('/apiv4/cohorts/<int:cohort_id>/file_manifest/', methods=['POST', 'GET'], strict_slashes=False)
def cohort_file_manifest(cohort_id):
    """
    GET: Retrieve a cohort's file manifest
    POST: Retrieve a cohort's file manifest with applied filters
    """

    response = None
    code = None

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'], cohort_id)

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            file_manifest = get_file_manifest(cohort_id, user)
            if file_manifest:
                response_obj = {}
                # Presence of a message means something went wrong with our request
                if 'message' in file_manifest:
                    code = 400
                else:
                    code = 200

                response_obj['data'] = file_manifest
                response_obj['code'] = code
                response = jsonify(response_obj)
                response.status_code = code
            else:
                response = jsonify({
                    'code': 500,
                    'message': "Error while attempting to retrieve file manifest for cohort {}.".format(str(cohort_id))
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
            'message': 'Encountered an error while attempting to identify this user.'
        })
        response.status_code = 500

    return response


@app.route('/apiv4/cohorts/preview/', methods=['POST'], strict_slashes=False)
def cohort_preview():
    """List the samples, cases, and counts a given set of cohort filters would produce"""

    response = None
    code = None

    try:
        cohort_counts = get_cohort_counts()
        
        if cohort_counts:
            response_obj = {}
            # Presence of a message means something went wrong with the filters we received
            if 'message' in cohort_counts:
                code = 400
            else:
                code = 200
    
            response_obj['data'] = cohort_counts
            response_obj['code'] = code
            response = jsonify(response_obj)
            response.status_code = code
                
        # Lack of a valid object means something went wrong on the server
        else:
            response = jsonify({
                'code': 500,
                'message': "Error while attempting to retrieve case and sample counts for these filters."
            })
            response.status_code = 500
            
    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to build this cohort preview.'
        })
        response.status_code = 500

    return response
