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

DJANGO_URI = os.getenv('DJANGO_URI')

MAX_FETCH_COUNT = 5000

def convert_to_bool(s):
    if s in ['True']:
        s = True
    elif s in ['False']:
        s = False
    return s


def get_auth():
    with open(
            join(dirname(__file__), '../{}{}'.format(os.environ.get('SECURE_LOCAL_PATH'), "dev.api_token.json"))) as f:
        api_token = f.read()
    auth = {"Authorization": "APIToken {}".format(api_token)}
    # auth = {"Authorization": "Token {}".format(api_token)}
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
                response = requests.post("{}/{}/".format(DJANGO_URI, 'cohorts/api/save_cohort'),
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
        results = requests.delete("{}/{}/".format(DJANGO_URI, 'cohorts/api/delete_cohort'),
                    params=path_params, json=data, headers=auth)
        cohort_list = results.json()
    except Exception as e:
        logger.exception(e)

    return cohort_list


def get_cohort_manifest(user, cohort_id):
    cohort_objects = None

    path_params = {
        "email": user,
        "access_class": "doi",
        "access_type": "gs",
        "region": "us",
        "fetch_count": 1000,
        "page": 1,
        "offset": 0}

    access_classes = ["url", "doi"]
    access_types = ["gs"]
    regions = ["us"]

    # Get and validate parameters
    for key in request.args.keys():
        if key in path_params:
            path_params[key] = request.args.get(key)
    path_params['fetch_count'] = int(path_params['fetch_count'])
    path_params['offset'] = int(path_params['offset'])
    path_params['page'] = int(path_params['page'])
    if path_params["fetch_count"] > MAX_FETCH_COUNT:
        cohort_objects = {
            "message": "Fetch count greater than {}".format(MAX_FETCH_COUNT),
            "code": 400
        }
    if path_params["offset"] < 0:
        cohort_objects = {
            "message": "Fetch offset {} must be non-negative integer".format(path_params['offset']),
            'code': 400
        }
    if path_params["access_class"] not in access_classes:
        cohort_objects = {
            "message": "Invalid access class {}".format(path_params['access_class']),
            'code': 400
        }
    if path_params['access_type'] not in access_types:
        cohort_objects = {
            "message": "Invalid access type {}".format(path_params['access_type']),
            'code': 400
        }
    if path_params['region'] not in regions:
        cohort_objects = {
            "message": "Invalid region {}".format(path_params['region']),
            'code': 400
        }
    if cohort_objects == None:
        path_params["page"] = int(path_params['page'])

        try:
            auth = get_auth()
            results = requests.get("{}/cohorts/api/{}/manifest/".format(DJANGO_URI, cohort_id),
                                params = path_params, headers=auth)
            cohort_objects = results.json()
        except Exception as e:
            logger.exception(e)

    return cohort_objects


def get_cohort_objects(user, cohort_id):
    cohort_objects = None

    path_params = {
        "email": user,
        "return_level": "Series",
        "fetch_count": 1000,
        "page": 1,
        "offset": 0}

    # Several parameters that we are not making available to users
    hidden_params= {
        "return_objects": True,
        "return_filter": True,
        "return_DOIs": False,
        "return_URLs": False,
        # "return_sql": False,
    }

    return_levels = [
        'Collection',
        'Instance',
        'Series',
        'Study',
        'Patient',
        'Instance'
    ]

    # Get and validate parameters
    for key in request.args.keys():
        if key in path_params:
            path_params[key] = request.args.get(key)
        else:
            cohort_objects = {
                "message": "Invalid key {}".format(key),
                'code': 400
            }
            return cohort_objects

    path_params['fetch_count'] = int(path_params['fetch_count'])
    path_params['offset'] = int(path_params['offset'])
    path_params['page'] = int(path_params['page'])
    # for s in ['return_objects', 'return_filter', 'return_DOIs', 'return_URLs']: # , 'return_sql']:
    #     path_params[s] = path_params[s] in [True, 'True']
    if path_params["fetch_count"] > MAX_FETCH_COUNT:
        cohort_objects = {
            "message": "Fetch count greater than {}".format(MAX_FETCH_COUNT),
            'code': 400
        }
    if path_params["offset"] < 0:
        cohort_objects = {
            "message": "Fetch offset {} must be non-negative integer".format(path_params['offset']),
            'code': 400
        }
    if path_params['return_level'] not in return_levels:
        cohort_objects = {
            "message": "Invalid return level {}".format(path_params['return_level']),
            'code': 400
        }
    if cohort_objects == None:
        path_params["page"] = int(path_params['page'])

        try:
            auth = get_auth()
            path_params.update(hidden_params)
            results = requests.get("{}/{}/{}/".format(DJANGO_URI, 'cohorts/api',cohort_id),
                                params = path_params, headers=auth)
            cohort_objects = results.json()
        except Exception as e:
            logger.exception(e)

    return cohort_objects


def post_cohort_preview():
    cohort_objects = None

    path_params = {
        "return_level": "Series",
        "fetch_count": 1000,
        "page": 1,
        "offset": 0}

    # Several parameters that we are not making available to users
    hidden_params= {
        "return_objects": True,
        "return_filter": True,
        "return_DOIs": False,
        "return_URLs": False,
        # "return_sql": False,
    }

    return_levels = [
        'Collection',
        'Instance',
        'Series',
        'Study',
        'Patient',
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
                    path_params[key] = request.args.get(key)
                else:
                    cohort_objects =dict(
                        message = "Invalid key {}".format(key),
                        code = 400
                    )
                    return cohort_objects

            path_params['fetch_count'] = int(path_params['fetch_count'])
            path_params['offset'] = int(path_params['offset'])
            path_params['page'] = int(path_params['page'])
            # for s in ['return_objects', 'return_filter', 'return_DOIs', 'return_URLs']: #, 'return_sql']:
            #     path_params[s] = path_params[s] in [True, 'True']
            if path_params["fetch_count"] > MAX_FETCH_COUNT:
                cohort_objects = dict(
                    message = "Fetch count greater than {}".format(MAX_FETCH_COUNT),
                    code = 400)
            if path_params["offset"] < 0:
                cohort_objects = dict(
                    message = "Fetch offset {} must be non-negative integer".format(path_params['offset']),
                    code = 400)
            if path_params['return_level'] not in return_levels:
                cohort_objects = dict(
                    message = "Invalid return level {}".format(path_params['return_level']),
                    code = 400)
            if cohort_objects == None:
                try:
                    auth = get_auth()
                    data = {"request_data": request_data}
                    path_params.update(hidden_params)
                    results = requests.post("{}/{}/".format(DJANGO_URI, 'cohorts/api/preview'),
                                           params=path_params, json=data, headers=auth)
                    pass
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
    cohort_objects = None

    path_params = {
        "access_class": "doi",
        "access_type": "gs",
        "region": "us",
        "fetch_count": 1000,
        "page": 1,
        "offset": 0}

    access_classes = ["url", "doi"]
    access_types = ["gs"]
    regions = ["us"]

    try:
        request_data = request.get_json()

        if 'filterSet' not in request_data:
            cohort_objects = dict(
                message='No filters were provided; ensure that the request body contains a \'filters\' property.')
        else:

            schema_validate(request_data['filterSet'], COHORT_FILTER_SCHEMA)

        # Get and validate parameters
        for key in request.args.keys():
            if key in path_params:
                path_params[key] = request.args.get(key)
            else:
                cohort_objects = {
                    "message": "Invalid key {}".format(key),
                    'code': 400
                }
        path_params['fetch_count'] = int(path_params['fetch_count'])
        path_params['offset'] = int(path_params['offset'])
        path_params['page'] = int(path_params['page'])
        if path_params["fetch_count"] > MAX_FETCH_COUNT:
            cohort_objects = {
                "message": "Fetch count greater than {}".format(MAX_FETCH_COUNT),
                "code": 400
            }
        if path_params["offset"] < 0:
            cohort_objects = {
                "message": "Fetch offset {} must be non-negative integer".format(path_params['offset']),
                'code': 400
            }
        if path_params["access_class"] not in access_classes:
            cohort_objects = {
                "message": "Invalid access class {}".format(path_params['access_class']),
                'code': 400
            }
        if path_params['access_type'] not in access_types:
            cohort_objects = {
                "message": "Invalid access type {}".format(path_params['access_type']),
                'code': 400
            }
        if path_params['region'] not in regions:
            cohort_objects = {
                "message": "Invalid region {}".format(path_params['region']),
                'code': 400
            }
        if cohort_objects == None:
            try:
                auth = get_auth()
                data = {"request_data": request_data}
                results = requests.post("{}/cohorts/api/preview/manifest/".format(DJANGO_URI),
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
        results = requests.get("{}/{}/".format(DJANGO_URI, 'cohorts/api'),
            params=path_params, headers=auth)
        cohort_list = results.json()
    except Exception as e:
        logger.exception(e)

    return cohort_list


# def get_file_manifest(cohort_id, user):
#     file_manifest = None
#     inc_filters = {}
#
#     try:
#         has_access = auth_dataset_whitelists_for_user(user.id)
#
#         params = {
#             'limit': settings.MAX_FILE_LIST_REQUEST,
#             'build': 'HG19',
#             'access': has_access
#         }
#
#         request_data = request.get_json()
#
#         param_set = {
#             'offset': {'default': 0, 'type': int, 'name': 'offset'},
#             'page': {'default': 1, 'type': int, 'name': 'page'},
#             'fetch_count': {'default': 5000, 'type': int, 'name': 'limit'},
#             'genomic_build': {'default': "HG19", 'type': str, 'name': 'build'}
#         }
#
#         for param, parameter in param_set.items():
#             default = parameter['default']
#             param_type = parameter['type']
#             name = parameter['name']
#             params[name] = request_data[param] if (request_data and param in request_data) else request.args.get(param, default=default, type=param_type) if param in request.args else default
#
#             if request_data:
#                 inc_filters = {
#                     filter: request_data[filter]
#                     for filter in request_data.keys()
#                     if filter not in list(param_set.keys())
#                 }
#
#         response = cohort_files(cohort_id, user=user, inc_filters=inc_filters, **params)
#
#         file_manifest = response['file_list'] if response and response['file_list'] else None
#
#     except BadRequest as e:
#         logger.warn("[WARNING] Received bad request - couldn't load JSON.")
#         file_manifest = {
#             'message': 'The JSON provided in this request appears to be improperly formatted.',
#         }
#     except Exception as e:
#         logger.error("[ERROR] File trieving the file manifest for Cohort {}:".format(str(cohort_id)))
#         logger.exception(e)
#
#     return file_manifest



