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
import re
import json
import requests

from flask import request
from werkzeug.exceptions import BadRequest

from python_settings import settings

from jsonschema import validate as schema_validate, ValidationError
from . schemas.filters import COHORT_FILTERS_SCHEMA
from . cohort_utils import get_manifest
from api.auth import get_auth

BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(settings.LOGGER_NAME)

MAX_FETCH_COUNT = 5000

def convert_to_bool(s):
    if s in ['True']:
        s = True
    elif s in ['False']:
        s = False
    return s


def get_params(param_defaults):
    params = {}
    for key in param_defaults:
        params[key] = request.args.get(key)
        if params[key] == None:
            params[key] = param_defaults[key]
    return params


def create_cohort(user):
    cohort_info = None

    try:
        request_data = request.get_json()
        if 'filters' not in request_data:
            return dict(
                message = 'No filters were provided; ensure that the request body contains a \'filters\' property.',
                code = 400)

        schema_validate(request_data['filters'], COHORT_FILTERS_SCHEMA)

        if 'name' not in request_data:
            return dict(
                message = 'A name was not provided for this cohort. The cohort was not made.',
                code = 400
            )

        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match = blacklist.search(str(request_data['name']))

        if not match and 'description' in request_data:
            match = blacklist.search(str(request_data['description']))

        if match:
            return dict(
                message = "Your cohort's name or description contains invalid characters; " +
                            "please edit them and resubmit. [Saw {}]".format(str(match)),
                code = 400
            )

        path_params = {'email': user}
        try:
            auth = get_auth()
            data = {"request_data": request_data}
            response = requests.post("{}/{}/".format(settings.BASE_URL, 'cohorts/api/save_cohort'),
                            params=path_params, json=data, headers=auth)
            cohort_info = response.json()
        except Exception as e:
            logger.exception(e)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        cohort_info = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
            'code': 400
        }

    except ValidationError as e:
        logger.warning("[WARNING] Cohort information rejected for improper formatting: {}".format(e))
        cohort_info = {
            'message': 'Cohort information was improperly formatted - cohort not created.',
            'code': 400
        }

    return cohort_info


def get_cohort_manifest(user, cohort_id):
    manifest_info = get_manifest(request,
                                 func=requests.get,
                                 url="{}/cohorts/api/{}/manifest/".format(settings.BASE_URL, cohort_id),
                                 user=user)

    return manifest_info


def get_cohort_preview_manifest():
    try:
        if 'next_page' in request.args and request.args['next_page'] not in ["", None]:
            data = {"request_data": None}
        else:
            request_data = request.get_json()

            if 'filters' not in request_data:
                return dict(
                    message = 'No filters were provided; ensure that the request body contains a \'filters\' property.',
                    code = 400)

            schema_validate(request_data['filters'], COHORT_FILTERS_SCHEMA)

            if 'name' not in request_data:
                return dict(
                    message = 'A name was not provided for this cohort. The cohort was not made.',
                    code = 400
                )

            blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
            match = blacklist.search(str(request_data['name']))

            if not match and 'description' in request_data:
                match = blacklist.search(str(request_data['description']))

            if match:
                return dict(
                    message = "Your cohort's name or description contains invalid characters; " +
                                "please edit them and resubmit. [Saw {}]".format(str(match)),
                    code = 400
                )

            data = {"request_data": request_data}
        manifest_info = get_manifest(request,
                             func=requests.post,
                             url="{}/cohorts/api/preview/manifest/".format(settings.BASE_URL),
                             data=data)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        manifest_info = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)

    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        manifest_info = dict(
            message= 'Filters were improperly formatted.',
            code = 400)

    return manifest_info


def get_cohort_list(user):
    cohort_list = None

    try:
        auth = get_auth()
        path_params = {'email': user}
        results = requests.get("{}/{}/".format(settings.BASE_URL, 'cohorts/api'),
            params=path_params, headers=auth)
        cohort_list = results.json()
    except Exception as e:
        logger.exception(e)

    return cohort_list


def delete_cohort(user, cohort_id):
    cohort_ids = {"cohorts": [cohort_id]}

    cohort_list = _delete_cohorts(user, cohort_ids)

    return cohort_list


def delete_cohorts(user):
    request_data = request.get_json()

    cohort_list = _delete_cohorts(user, request_data)

    return cohort_list


def _delete_cohorts(user, cohort_ids):
    cohort_list = None

    try:
        # Validate the list of ids
        for id in cohort_ids['cohorts']:
            assert type(id) == int
        auth = get_auth()
        path_params = {'email': user}
        data = {"cohort_ids": cohort_ids}
        results = requests.delete("{}/{}/".format(settings.BASE_URL, 'cohorts/api/delete_cohort'),
                    params=path_params, json=data, headers=auth)
        cohort_list = results.json()
    except Exception as e:
        logger.exception(e)

    return cohort_list





