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
from .query_utils import perform_query, query_next_page
from jsonschema import validate as schema_validate, ValidationError
# from . schemas.querypreviewbody import QUERY_PREVIEW_BODY
# from . schemas.filters import COHORT_FILTERS_SCHEMA
from .schemas.queryfields import QUERY_FIELDS
from .cohort_utils import validate_cohort_definition
from .version_config import API_VERSION

BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(settings.LOGGER_NAME)

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


def post_query(user, cohort_id):
    try:
        request_data = request.get_json()

        if 'fields' not in request_data:
            return dict(
                message = 'No fields provided; ensure that the request body contains a \'fields\' component.',
                code = 400)

        schema_validate(request_data, QUERY_FIELDS)

        data = {
            "request_data": request_data,
            "email": user
        }

        query_info = perform_query(request,
                             func=requests.post,
                             url=f"{settings.BASE_URL}/cohorts/api/{API_VERSION}/{cohort_id}/query/",
                             data=data,
                             user=user)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        query_info = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)

    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        query_info = dict(
            message= 'Filters were improperly formatted.',
            code = 400)

    return query_info


def post_query_preview(user):
    try:
        request_data = request.get_json()
        request_data['cohort_def'], cohort_info = validate_cohort_definition(request_data['cohort_def'])
        if 'message' in cohort_info:
            return cohort_info
        data = {
            "request_data": request_data,
        }
        query_info = perform_query(request,
                             func=requests.post,
                             url=f"{settings.BASE_URL}/cohorts/api/{API_VERSION}/preview/query/",
                             data=data,
                             user=user)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        query_info = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)

    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        query_info = dict(
            message= 'Filters were improperly formatted.',
            code = 400)

    return query_info


def get_query_next_page(user):
    query_info = query_next_page(request, user)
    return query_info






