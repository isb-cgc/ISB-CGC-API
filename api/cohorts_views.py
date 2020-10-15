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
import os
from os.path import join, dirname
import requests

from flask import request
from werkzeug.exceptions import BadRequest

from python_settings import settings

from jsonschema import validate as schema_validate, ValidationError
from . schemas.filterset import COHORT_FILTER_SCHEMA

BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(settings.LOGGER_NAME)

MAX_FETCH_COUNT = 5000

def convert_to_bool(s):
    if s in ['True']:
        s = True
    elif s in ['False']:
        s = False
    return s


def get_auth():
    auth = {"Authorization": "APIToken {}".format(settings.API_AUTH_TOKEN)}
    return auth


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
        schema_validate(request_data['filterSet'], COHORT_FILTER_SCHEMA)

        if 'name' not in request_data:
            cohort_info = {
                'message': 'A name was not provided for this cohort. The cohort was not made.',
            }
            return cohort_info

        if 'filterSet' not in request_data:
            cohort_info = {
                'message': 'Filters were not provided; at least one filter must be provided for a cohort to be valid.' +
                       ' The cohort was not made.',
            }
            return cohort_info

        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match = blacklist.search(str(request_data['name']))

        if not match and 'description' in request_data:
            match = blacklist.search(str(request_data['description']))

        if match:
            cohort_info = {
                'message': 'Your cohort\'s name or description contains invalid characters; please edit them and resubmit. ' +
                    '[Saw {}]'.format(str(match)),
            }

        else:
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
        logger.warn("[WARNING] Received bad request - couldn't load JSON.")
        cohort_info = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
            'code': 400
        }

    except ValidationError as e:
        logger.warn("[WARNING] Cohort information rejected for improper formatting: {}".format(e))
        cohort_info = {
            'message': 'Cohort information was improperly formatted - cohort not created.',
            'code': 400
        }

    return cohort_info


def delete_cohort(user, cohort_id):
    cohort_ids = [cohort_id]

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
        for id in cohort_ids:
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


def get_cohort_manifest(user, cohort_id):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    cohort_objects = None

    path_params = {
        "email": user,
        "access_method": "doi",
        "url_access_type": "gs",
        "url_region": "us",
        "job_reference": None,
        "next_page": ""}

    access_methodes = ["url", "doi"]
    url_access_types = ["gs"]
    url_regions = ["us"]

    # Get and validate parameters
    for key in request.args.keys():
        match = blacklist.search(str(key))
        if match:
            return dict(
                message = "Key {} contains invalid characters; please edit and resubmit. " +
                           "[Saw {}]".format(str(key, match)),
                code = 400
            )
        if key in path_params:
            path_params[key] = request.args.get(key)
    if path_params["access_method"] not in access_methodes:
        return dict(
            message = "Invalid access_method {}".format(path_params['access_method']),
            code = 400
        )
    if path_params['url_access_type'] not in url_access_types:
        return dict(
            message = "Invalid url_access_type {}".format(path_params['url_access_type']),
            code = 400
        )
    if path_params['url_region'] not in url_regions:
        return dict(
            message = "Invalid url_region {}".format(path_params['url_region']),
            code = 400
        )
    if cohort_objects == None:

        try:
            auth = get_auth()
            results = requests.get("{}/cohorts/api/{}/manifest/".format(settings.BASE_URL, cohort_id),
                                params = path_params, headers=auth)
            cohort_objects = results.json()
        except Exception as e:
            logger.exception(e)

    return cohort_objects


def get_cohort_objects(user, cohort_id):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    cohort_objects = None

    path_params = {
        "email": user,
        "return_level": "Series",
        "return_sql": False,
        "job_reference": {},
        "next_page": ""}

    # Several parameters that we are not making available to users
    hidden_params= {
        # "return_objects": True,
        "return_filter": True,
        # "return_DOIs": False,
        # "return_URLs": False,
    }

    return_levels = [
        'None',
        'Collection',
        'Patient',
        'Study',
        'Series',
        'Instance'
    ]

    # Get and validate parameters
    for key in request.args.keys():
        match = blacklist.search(str(key))
        if match:
            return dict(
                message = "Key {} contains invalid characters; please edit and resubmit. " +
                           "[Saw {}]".format(str(key, match)),
                code = 400
            )
        if key in path_params:
            path_params[key] = request.args.get(key)
        else:
            cohort_objects = {
                "message": "Invalid key {}".format(key),
                'code': 400
            }
            return cohort_objects

    # path_params['fetch_count'] = int(path_params['fetch_count'])
    # path_params['offset'] = int(path_params['offset'])
    # path_params['page'] = int(path_params['page'])
    for s in ['return_sql']: # 'return_objects', 'return_filter', 'return_DOIs', 'return_URLs']: # ,
        if s in path_params:
            path_params[s] = path_params[s] in [True, 'True']
    # if path_params["fetch_count"] > MAX_FETCH_COUNT:
    #     return dict(
    #         message = "Fetch count greater than {}".format(MAX_FETCH_COUNT),
    #         code = 400
    #     )
    # if path_params["offset"] < 0:
    #     return dict(
    #         message = "Fetch offset {} must be non-negative integer".format(path_params['offset']),
    #         code = 400
    #     )
    if path_params['return_level'] not in return_levels:
        return dict(
            message = "Invalid return level {}".format(path_params['return_level']),
            code = 400
        )
    if cohort_objects == None:
        # path_params["page"] = int(path_params['page'])

        try:
            auth = get_auth()
            path_params.update(hidden_params)
            results = requests.get("{}/{}/{}/".format(settings.BASE_URL, 'cohorts/api',cohort_id),
                                params = path_params, headers=auth)
            cohort_objects = results.json()
        except Exception as e:
            logger.exception(e)

    return cohort_objects


def post_cohort_preview():
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    cohort_objects = None

    path_params = {
        "return_level": "Series",
        "return_sql": False,
        "job_reference": {},
        "next_page": ""}
        # "fetch_count": 1000,
        # "page": 1,
        # "offset": 0}

    # Several parameters that we are not making available to users
    hidden_params= {
        # "return_objects": True,
        "return_filter": True,
        # "return_DOIs": False,
        # "return_URLs": False,
    }

    return_levels = [
        'None',
        'Collection',
        'Patient',
        'Study',
        'Series',
        'Instance'
    ]

    try:
        request_data = request.get_json()
        schema_validate(request_data['filterSet'], COHORT_FILTER_SCHEMA)

        if 'filterSet' not in request_data:
            cohort_objects = dict(
                message = 'No filters were provided; ensure that the request body contains a \'filters\' property.',
                code = 400)
        else:

            # Get and validate parameters
            # Get and validate parameters
            for key in request.args.keys():
                if key in path_params:
                    match = blacklist.search(str(key))
                    if match:
                        return dict(
                            message="Key {} contains invalid characters; please edit and resubmit. " +
                                    "[Saw {}]".format(str(key, match)),
                            code=400
                        )
                    path_params[key] = request.args.get(key)
                else:
                    cohort_objects =dict(
                        message = "Invalid key {}".format(key),
                        code = 400
                    )
                    return cohort_objects

            # path_params['fetch_count'] = int(path_params['fetch_count'])
            # path_params['offset'] = int(path_params['offset'])
            # path_params['page'] = int(path_params['page'])
            for s in ['return_sql']: #'return_objects', 'return_filter', 'return_DOIs', 'return_URLs']:
                if s in path_params:
                    path_params[s] = path_params[s] in [True, 'True']
            # if path_params["fetch_count"] > MAX_FETCH_COUNT:
            #     return dict(
            #         message="Fetch count greater than {}".format(MAX_FETCH_COUNT),
            #         code=400
            #     )
            # if path_params["offset"] < 0:
            #     return dict(
            #         message="Fetch offset {} must be non-negative integer".format(path_params['offset']),
            #         code=400
            #     )
            if path_params['return_level'] not in return_levels:
                return dict(
                    message="Invalid return level {}".format(path_params['return_level']),
                    code=400
                )
            if cohort_objects == None:
                try:
                    auth = get_auth()
                    data = {"request_data": request_data}
                    path_params.update(hidden_params)
                    results = requests.post("{}/{}/".format(settings.BASE_URL, 'cohorts/api/preview'),
                                           params=path_params, json=data, headers=auth)
                    cohort_objects = results.json()
                except Exception as e:
                    logger.exception(e)

        return cohort_objects

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        cohort_objects = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)
    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        cohort_objects = dict(
            message= 'Filters were improperly formatted.',
            code = 400)
    except Exception as e:
        logger.exception(e)
        cohort_objects = dict(
            message = '[ERROR] Error trying to preview a cohort',
            code = 400)

    return cohort_objects


def get_cohort_preview_manifest():
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    cohort_objects = None

    path_params = {
        "access_method": "doi",
        "url_access_type": "gs",
        "url_region": "us",
        "job_reference": None,
        "next_page": ""}

    access_methods = ["url", "doi"]
    url_access_types = ["gs"]
    url_regions = ["us"]

    try:
        request_data = request.get_json()

        if 'filterSet' not in request_data:
            cohort_objects = dict(
                message='No filters were provided; ensure that the request body contains a \'filters\' property.')
        else:

            schema_validate(request_data['filterSet'], COHORT_FILTER_SCHEMA)

        # Get and validate parameters
        for key in request.args.keys():
            match = blacklist.search(str(key))
            if match:
                return dict(
                    message="Key {} contains invalid characters; please edit and resubmit. " +
                            "[Saw {}]".format(str(key, match)),
                    code=400
                )
            if key in path_params:
                path_params[key] = request.args.get(key)
            else:
                cohort_objects = {
                    "message": "Invalid key {}".format(key),
                    'code': 400
                }
        if path_params["access_method"] not in access_methods:
            return dict(
                message="Invalid access_method {}".format(path_params['access_method']),
                code=400
            )
        if path_params['url_access_type'] not in url_access_types:
            return dict(
                message="Invalid url_access_type {}".format(path_params['url_access_type']),
                code=400
            )
        if path_params['url_region'] not in url_regions:
            return dict(
                message="Invalid url_region {}".format(path_params['url_region']),
                code=400
            )
        if cohort_objects == None:
            try:
                auth = get_auth()
                data = {"request_data": request_data}
                results = requests.post("{}/cohorts/api/preview/manifest/".format(settings.BASE_URL),
                                    params = path_params, json=data, headers=auth)
                cohort_objects = results.json()
            except Exception as e:
                logger.exception(e)

        return cohort_objects

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        cohort_objects = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)
    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        cohort_objects = dict(
            message= 'Filters were improperly formatted.',
            code = 400)
    except Exception as e:
        logger.exception(e)
        cohort_objects = dict(
            message = '[ERROR] Error trying to preview a cohort',
            code = 400)

    return cohort_objects


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



