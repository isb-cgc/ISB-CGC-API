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
import requests

from flask import request
from werkzeug.exceptions import BadRequest
from python_settings import settings
from api.cohort_utils import get_manifest, get_manifest_nextpage, validate_cohort_definition
from api.auth import get_auth

from jsonschema import validate as schema_validate, ValidationError
from . schemas.filters import COHORT_FILTERS_SCHEMA
import re

logger = logging.getLogger(settings.LOGGER_NAME)
BLACKLIST_RE = settings.BLACKLIST_RE
MAX_FETCH_COUNT = 5000


def create_cohort(user):
    try:
        # path_params = {'email': user}
        try:
            request_data, cohort_info = validate_cohort_definition(request.get_json())
            if 'message' in cohort_info:
                return cohort_info

            auth = get_auth()
            data = {
                "request_data": request_data,
                "email": user
            }
            response = requests.post("{}/{}/".format(settings.BASE_URL, 'cohorts/api/save_cohort'),
                            json=data, headers=auth)
                            # params = path_params, json = data, headers = auth)
            cohort_info = response.json()
        except Exception as e:
            logger.exception(e)
            cohort_info = {
                'message': f'[WARNING] {e}',
                'code': 400
            }
    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        cohort_info = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
            'code': 400
        }
    except Exception as e:
        logger.warning(f"Error {e} validating filterset.")
        cohort_info = {
            'message': e.message,
            'code': 400
        }
    return cohort_info


def get_cohort_manifest(user, cohort_id):
    data = {
        "email": user
    }
    manifest_info = get_manifest(request,
                                 func=requests.get,
                                 url="{}/cohorts/api/{}/manifest/".format(settings.BASE_URL, cohort_id),
                                 data = data)
                                 # user=user)
    return manifest_info

def get_cohort_preview_manifest(user):
    try:
        request_data, cohort_info = validate_cohort_definition(request.get_json())
        if 'message' in cohort_info:
            return cohort_info
        data = {
            "request_data": request_data,
            "email": user
        }
        manifest_info = get_manifest(request, func=requests.post,
                             url="{}/cohorts/api/preview/manifest/".format(settings.BASE_URL), data=data)
                             # user=user)
    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        manifest_info = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)

    return manifest_info


def get_cohort_manifest_nextpage(user):
    manifest_info = get_manifest_nextpage(request, user=user)
    return manifest_info


def get_cohort_list(user):
    cohort_list = None

    try:
        auth = get_auth()
        # path_params = {'email': user}
        data = {'email': user}
        results = requests.get("{}/{}/".format(settings.BASE_URL, 'cohorts/api'),
            json=data, headers=auth)
            # params = path_params, headers = auth)
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
        # path_params = {'email': user}
        data = {
            "cohort_ids": cohort_ids,
            "email": user
        }
        results = requests.delete("{}/{}/".format(settings.BASE_URL, 'cohorts/api/delete_cohort'),
                    # params=path_params, json=data, headers=auth)
                   json=data, headers=auth)
        cohort_list = results.json()
    except Exception as e:
        logger.exception(e)

    return cohort_list





