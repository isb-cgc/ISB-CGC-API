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
from . schemas.filterset import COHORT_FILTER_SCHEMA
from . cohort_utils import submit_BQ_job, get_objects, get_manifest
from .auth import get_auth

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



def get_cohort_objects(user, cohort_id):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    cohort_objects = None

    path_params = {
        "email": user,
        "return_level": "Series",
        "return_sql": False,
     }

    local_params = {
        "job_reference": {},
        "next_page": "",
        "page_size": 10000
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
                message="Key {} contains invalid characters; please edit and resubmit. " +
                        "[Saw {}]".format(str(key, match)),
                code=400
            )
        if key in path_params:
            path_params[key] = request.args.get(key)
        elif key in local_params:
            local_params[key] = request.args.get(key)
        else:
            cohort_objects =dict(
                message = "Invalid key {}".format(key),
                code = 400
            )
            return cohort_objects

    local_params['page_size'] = int(local_params['page_size'])
    for s in ['return_sql']:
        if s in path_params:
            path_params[s] = path_params[s] in [True, 'True']
    if path_params['return_level'] not in return_levels:
        return dict(
            message="Invalid return level {}".format(path_params['return_level']),
            code=400
        )
    if cohort_objects == None:
        try:
            if local_params["job_reference"] and local_params['next_page']:
                job_reference = json.loads(local_params["job_reference"].replace("'",'"'))
                # We don't return the project ID to the user
                job_reference['projectId'] = settings.BIGQUERY_PROJECT_ID
                next_page = local_params['next_page']
                cohort_objects = dict(
                    cohort = {},
                    job_reference = job_reference,
                    next_page = next_page
                )
            else:
                auth = get_auth()
                results = requests.get("{}/{}/{}/".format(settings.BASE_URL, 'cohorts/api', cohort_id),
                                       params=path_params, headers=auth)
                cohort_objects = results.json()

                if "message" in cohort_objects:
                    return cohort_objects

                # Get the BQ SQL string and params from the webapp
                if path_params['return_level'] != 'None':
                    cohort_objects['job_reference'] = submit_BQ_job(cohort_objects['query']['sql_string'],
                                                                    cohort_objects['query']['params'])

                # Don't return the query in this form
                cohort_objects.pop('query')

                # job_reference = cohort_data['job_reference']
                cohort_objects['next_page'] = None

            if path_params['return_level']!= 'None':
                cohort_objects = get_objects(path_params['return_level'], cohort_objects, local_params['page_size'])
                # We don't return the project ID to the user
                cohort_objects['job_reference'].pop('projectId')
            else:
                cohort_objects['cohortObjects'] = dict(
                    totalFound = 0,
                    rowsReturned = 0,
                    collections = [],
                )
        except Exception as e:
            logger.exception(e)


    return cohort_objects


def get_cohort_manifest(user, cohort_id):
    manifest_info = get_manifest(request,
                                 func=requests.get,
                                 url="{}/cohorts/api/{}/manifest/".format(settings.BASE_URL, cohort_id),
                                 user=user)

    return manifest_info


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


def post_cohort_preview():
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    cohort_objects = None

    path_params = {
        "return_level": "Series",
        "return_sql": False,
     }

    local_params = {
        "job_reference": {},
        "next_page": "",
        "page_size": 10000
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
                elif key in local_params:
                    if match:
                        return dict(
                            message="Key {} contains invalid characters; please edit and resubmit. " +
                                    "[Saw {}]".format(str(key, match)),
                            code=400
                        )
                    local_params[key] = request.args.get(key)
                else:
                    cohort_objects =dict(
                        message = "Invalid key {}".format(key),
                        code = 400
                    )
                    return cohort_objects

            local_params['page_size'] = int(local_params['page_size'])
            for s in ['return_sql']: #'return_objects', 'return_filter', 'return_DOIs', 'return_URLs']:
                if s in path_params:
                    path_params[s] = path_params[s] in [True, 'True']
            if path_params['return_level'] not in return_levels:
                return dict(
                    message="Invalid return level {}".format(path_params['return_level']),
                    code=400
                )
            if cohort_objects == None:
                try:
                    if local_params["job_reference"] and local_params['next_page']:
                        job_reference = json.loads(local_params["job_reference"].replace("'",'"'))
                        # We don't return the project ID to the user
                        job_reference['projectId'] = settings.BIGQUERY_PROJECT_ID
                        next_page = local_params['next_page']
                        cohort_objects = dict(
                            cohort = {},
                            job_reference = job_reference,
                            next_page = next_page
                        )
                    else:
                        auth = get_auth()
                        data = {"request_data": request_data}
                        results = requests.post("{}/{}/".format(settings.BASE_URL, 'cohorts/api/preview'),
                                               params=path_params, json=data, headers=auth)
                        cohort_objects = results.json()
                        print(("[STATUS] cohort_objects with sql_string and params: {}").format(cohort_objects))

                        if "message" in cohort_objects:
                            return cohort_objects

                        # Get the BQ SQL string and params from the webapp
                        if path_params['return_level'] != 'None':
                            cohort_objects['job_reference'] = submit_BQ_job(cohort_objects['query']['sql_string'],
                                                                        cohort_objects['query']['params'])
                            print(("[STATUS] cohort_objects with job_ref: {}").format(cohort_objects))
                        # Don't return the query in this form
                        cohort_objects.pop('query')

                        # job_reference = cohort_data['job_reference']
                        cohort_objects['next_page'] = None

                    if path_params['return_level']!= 'None':
                        cohort_objects = get_objects(path_params['return_level'], cohort_objects, local_params['page_size'])
                        # We don't return the project ID to the user
                        cohort_objects['job_reference'].pop('projectId')
                    else:
                        cohort_objects['cohortObjects'] = dict(
                            totalFound = 0,
                            rowsReturned = 0,
                            collections = [],
                        )
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
    try:
        request_data = request.get_json()

        if 'filterSet' not in request_data:
            manifest_info = dict(
                message='No filters were provided; ensure that the request body contains a \'filters\' property.')
        else:
            schema_validate(request_data['filterSet'], COHORT_FILTER_SCHEMA)
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





