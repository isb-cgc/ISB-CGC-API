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
from cohorts_views import get_cohort_info, get_cohorts, get_file_manifest, validate_user
from auth import auth_info
from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/apiv4', methods=['GET', 'POST'])
def base():
    """Base response"""
    response = jsonify({
        'code': 200,
        'message': 'Welcome to the ISB-CGC API, Version 4.'
    })
    response.status_code = 200
    return response


@app.route('/apiv4/cohorts/<int:cohort_id>', methods=['GET'])
def cohort(cohort_id):
    """Retrieve extended information for a specific cohort"""
    user_info = auth_info()
    logger.info("[STATUS] User info: {}".format(str(user_info)))
    user = validate_user(user_info['email'], cohort_id)

    response = None

    if not user:
        response = jsonify({
            'code': 403,
            'message': "User {} does not have access to cohort ID {}".format(user_info['email'] if 'email' in user_info else 'Anonymous',str(cohort_id))})
        response.status_code = 403

    else:
        cohort_info = get_cohort_info(cohort_id)
        if cohort_info:
            response = jsonify({
                'code': 200,
                'data': jsonify(cohort_info)
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 404,
                'message': "Cohort ID {} was not found.".format(str(cohort_id))})
            response.status_code = 404

    return response


@app.route('/apiv4/cohorts', methods=['GET'])
def cohorts():
    """Retrieve a user's list of cohorts"""
    user_info = auth_info()

    cohort_list = get_cohorts(user_info['email'])

    response = None

    if not cohort_list:
        response = jsonify({
            'code': 404,
            'message': "No cohorts were found for user {}".format(user_info['email'])})
        response.status_code = 404

    else:
        cohort_info = get_cohort_info(cohort_id)
        if cohort_info:
            response = jsonify({
                'code': 200,
                'data': jsonify(cohort_info)
            })
            response.status_code = 200

    return response


@app.route('/apiv4/cohorts/<int:cohort_id>/file_manifest', methods=['POST', 'GET'])
def cohort_file_manifest(cohort_id):
    """Retrieve a cohort's file manifest"""
    user_info = auth_info()
    user = validate_user(user_info['email'], cohort_id)

    response = None

    if not user:
        response = jsonify({
            'code': 403,
            'message': "User {} does not have access to cohort ID {}".format(user_info['email'],str(cohort_id))})
        response.status_code = 403

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
                'message': "Error while attempting to retrieve file manifest for cohort {}.".format(str(cohort_id))})
            response.status_code = 500

    return response
