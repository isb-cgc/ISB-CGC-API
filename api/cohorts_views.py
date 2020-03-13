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
import requests

from flask import request
from werkzeug.exceptions import BadRequest

from django.conf import settings

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


def delete_cohort(cohort_id):
    cohort_list = None

    cohort_ids = [cohort_id]

    cohort_list = _delete_cohorts(cohort_ids)

    return cohort_list


def delete_cohorts():
    cohort_list = None

    request_data = request.get_json()

    cohort_list = _delete_cohorts(request_data)

    return cohort_list

def _delete_cohorts(cohort_ids):
    cohort_list = None

    try:
        # Validate the list of ids
        for id in cohort_ids:
            assert type(id) == int
        params = {"user_name": "bill", "cohort_ids": cohort_ids}
        results = requests.delete("{}/{}/".format(DJANGO_URI, 'cohorts/api/delete_cohort'),
                                         json=params)
        cohort_list = results.json()
    except Exception as e:
        logger.exception(e)

    return cohort_list


def get_cohort_objects(cohort_id):
    cohort_objects = None

    request_string = {
        "user_name": "bill",
        "return_objects": True,
        "return_level":"Series",
        "return_filter":True,
        "return_DOIs":True,
        "return_URLs":True,
        "return_sql":False,
        "fetch_count":1000,
        "page":1,
        "offset":0}

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
        request_string[key] = request.args.get(key)
    request_string['fetch_count'] = int(request_string['fetch_count'])
    request_string['offset'] = int(request_string['offset'])
    request_string['page'] = int(request_string['page'])
    for s in ['return_objects', 'return_filter', 'return_DOIs', 'return_URLs', 'return_sql']:
        request_string[s] = request_string[s] in [True, 'True']
    if request_string["fetch_count"] > MAX_FETCH_COUNT:
        cohort_objects = {
            "message": "Fetch count greater than {}".format(MAX_FETCH_COUNT)
        }
    if request_string["offset"] < 0:
        cohort_objects = {
            "message": "Fetch offset {} must be non-negative integer".format(request_string('offset'))
        }
    if request_string['return_level'] not in return_levels:
        cohort_objects = {
            "message": "Invalid return level {}".format(request_string['return_level'])
        }
    # if request_string['return_filter'] not in [True,False]:
    #     cohort_objects = {
    #         "message": "Invalid return filter {}".format(request_string['return_filter'])
    #     }
    # if request_string['return_DOIs'] not in [True,False]:
    #     cohort_objects = {
    #         "message": "Invalid return DOIs {}".format(request_string['return_DOIs'])
    #     }
    # if request_string['return_URLs'] not in [True,False]:
    #     cohort_objects = {
    #         "message": "Invalid return URLs {}".format(request_string['return_URLs'])
    #     }
    if cohort_objects == None:
        request_string["page"] = int(request_string['page'])

        try:
            results = requests.get("{}/{}/{}/".format(DJANGO_URI, 'cohorts/api/objects',cohort_id),
                                params = request_string)
            cohort_objects = results.json()
        except Exception as e:
            logger.exception(e)

    return cohort_objects


def post_cohort_preview():

    result = None

    try:
        request_data = request.get_json()
        schema_validate(request_data, COHORT_FILTER_SCHEMA)

        if 'filter' not in request_data:
            cohort = {
                'message': 'No filters were provided; ensure that the request body contains a \'filters\' property.'
            }
        else:
            param_defaults = {
                "case_insensitive":True,
                "include_filter":True,
                "include_files":True,
                "include_DOIs":True,
                "include_URLs":True,
                "fetch_count":5000,
                "page":1,
                "offset":0
            }

            params = get_params(param_defaults)
            try:
                result = requests.post("{}/{}".format(DJANGO_URI, 'cohort/api/preview'),
                            json = request_data,
                            params = params)
            except:
                if result.status_code != 200:
                   raise Exception("oops!")

    except BadRequest as e:
        logger.warn("[WARNING] Received bad request - couldn't load JSON.")
        result = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }
    except ValidationError as e:
        logger.warn('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        result = {
            'message': 'Filters were improperly formatted.'
        }
    except Exception as e:
        logger.exception(e)

    return result


def get_cohort_list(user=None):
    cohort_list = None

    try:
        params = {"user_name": "bill"}
        results = requests.get("{}/{}/".format(DJANGO_URI, 'cohorts/api'),
                                    json=params)
        cohort_list = results.json()
    except Exception as e:
        logger.exception(e)

    return cohort_list


def create_cohort(user):
    cohort_info = None

    try:
        request_data = request.get_json()
        schema_validate(request_data, COHORT_FILTER_SCHEMA)

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
            try:
                data = {"user_name":"bill", "request_data":request_data}
                response = requests.post("{}/{}/".format(DJANGO_URI, 'cohorts/api/save_cohort'),
                                json = data)
                cohort_info = response.json()
            except Exception as e:
                logger.exception(e)

    except BadRequest as e:
        logger.warn("[WARNING] Received bad request - couldn't load JSON.")
        cohort_info = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }

    except ValidationError as e:
        logger.warn("[WARNING] Cohort information rejected for improper formatting: {}".format(e))
        cohort_info = {
            'message': 'Cohort information was improperly formatted - cohort not edited.',
        }

    return cohort_info


def get_params(param_defaults):
    params = {}
    for key in param_defaults:
        params[key] = request.args.get(key)
        if params[key] == None:
            params[key] = param_defaults[key]
    return params

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

# def post_create_cohort():
#
#     preview = None
#
#     try:
#         request_data = request.get_json()
#         schema_validate(request_data, COHORT_FILTER_SCHEMA)
#
#         if 'filter' not in request_data:
#             cohort = {
#                 'message': 'No filters were provided; ensure that the request body contains a \'filters\' property.'
#             }
#         else:
#             param_defaults = {
#                 "case_insensitive":True,
#                 "include_filter":True,
#                 "include_files":True,
#                 "include_DOIs":True,
#                 "include_URLs":True,
#                 "fetch_count":5000,
#                 "page":1,
#                 "offset":0
#             }
#
#             params = get_params(param_defaults)
#             try:
#                 result = requests.post("{}/{}".format(DJANGO_URI, 'cohort/api/save_cohort'),
#                             json = request_data,
#                             params = params)
#             except:
#                 if result.status_code != 200:
#                    raise Exception("oops!")
#             #response = result.json()
#             return result
#
#     except BadRequest as e:
#         logger.warn("[WARNING] Received bad request - couldn't load JSON.")
#         cohort_counts = {
#             'message': 'The JSON provided in this request appears to be improperly formatted.',
#         }
#     except ValidationError as e:
#         logger.warn('[WARNING] Filters rejected for improper formatting: {}'.format(e))
#         cohort_counts = {
#             'message': 'Filters were improperly formatted.'
#         }
#     except Exception as e:
#         logger.exception(e)
#
#     return cohort

# def get_cohort_info(cohort_id, get_barcodes=False):
#     cohort = None
#     try:
#         cohort_obj = Cohort.objects.get(id=cohort_id)
#         cohort = {
#             'id': cohort_obj.id,
#             'name': cohort_obj.name,
#             'case_count': cohort_obj.case_size(),
#             'sample_count': cohort_obj.sample_size(),
#             'programs': cohort_obj.get_program_names(),
#             'filters': cohort_obj.get_current_filters(True)
#         }
#
#         if get_barcodes:
#             cohort['barcodes'] = get_sample_case_list_bq(cohort_id)
#
#     except ObjectDoesNotExist as e:
#         logger.warn("Cohort with ID {} was not found!".format(str(cohort_id)))
#     except Exception as e:
#         logger.exception(e)
#
#     return cohort


