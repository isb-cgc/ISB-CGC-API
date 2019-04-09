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
from cohorts_views import get_cohort_info, get_cohorts, get_file_manifest, get_cohort_counts, validate_user, create_cohort, edit_cohort, UserValidationException
from auth import auth_info
from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/apiv4/cohorts/<int:cohort_id>/', methods=['GET', 'PATCH'], strict_slashes=False)
def cohort(cohort_id):
    """
    GET: Retrieve extended information for a specific cohort
    PATCH: Edit an extent cohort
    """

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'], cohort_id)

        response = None

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            if request.method == 'GET':
                cohort_info = get_cohort_info(cohort_id)
            else:
                cohort_info = edit_cohort(cohort_id)

            if cohort_info:
                response = jsonify({
                    'code': 200,
                    'data': cohort_info
                })
                response.status_code = 200
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

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'])

        response = None
        info = None

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
                if 'msg' in info:
                    # Presence of a message means something was wrong.
                    response = jsonify({
                        'code': 400,
                        'data': info
                    })
                    response.status_code = 400
                else:
                    response = jsonify({
                        'code': 200,
                        'data': info
                    })
                    response.status_code = 200
                # Lack of a valid object means something went wrong on the server
            else:
                response = jsonify({
                    'code': 500,
                    'message': "Error while attempting to create this cohort."
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

    try:
        user_info = auth_info()
        user = validate_user(user_info['email'], cohort_id)

        response = None

        if not user:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while attempting to identify this user.'
            })
            response.status_code = 500
        else:
            file_manifest = get_file_manifest(cohort_id, user)
            if file_manifest:
                response = jsonify({
                    'code': 200,
                    'data': file_manifest
                })
                response.status_code = 200
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

    cohort_counts = get_cohort_counts()
    
    if cohort_counts:
        # Presence of a message means something went wrong with the filters we received
        if 'msg' in cohort_counts:
            response = jsonify({
                'code': 400,
                'data': cohort_counts
            })
            response.status_code = 400
        else:
            response = jsonify({
                'code': 200,
                'data': cohort_counts
            })
            response.status_code = 200
    # Lack of a valid object means something went wrong on the server
    else:
        response = jsonify({
            'code': 500,
            'message': "Error while attempting to retrieve case and sample counts for these filters."
        })
        response.status_code = 500

    return response
