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
import json
import django
import re
import os
import requests

from flask import request
from werkzeug.exceptions import BadRequest

from django.contrib.auth.models import User as Django_User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings

from cohorts.models import Cohort_Perms, Cohort, Filters
#from cohorts.utils import get_sample_case_list_bq
from idc_collections.models import Program

from jsonschema import validate as schema_validate, ValidationError
from . schemas.filterset import COHORT_FILTER_SCHEMA

BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(settings.LOGGER_NAME)

DJANGO_URI = os.getenv('DJANGO_URI')

def get_file_manifest(cohort_id, user):
    file_manifest = None
    inc_filters = {}

    try:
        has_access = auth_dataset_whitelists_for_user(user.id)

        params = {
            'limit': settings.MAX_FILE_LIST_REQUEST,
            'build': 'HG19',
            'access': has_access
        }

        request_data = request.get_json()

        param_set = {
            'offset': {'default': 0, 'type': int, 'name': 'offset'},
            'page': {'default': 1, 'type': int, 'name': 'page'},
            'fetch_count': {'default': 5000, 'type': int, 'name': 'limit'},
            'genomic_build': {'default': "HG19", 'type': str, 'name': 'build'}
        }

        for param, parameter in param_set.items():
            default = parameter['default']
            param_type = parameter['type']
            name = parameter['name']
            params[name] = request_data[param] if (request_data and param in request_data) else request.args.get(param, default=default, type=param_type) if param in request.args else default

            if request_data:
                inc_filters = {
                    filter: request_data[filter]
                    for filter in request_data.keys()
                    if filter not in list(param_set.keys())
                }

        response = cohort_files(cohort_id, user=user, inc_filters=inc_filters, **params)

        file_manifest = response['file_list'] if response and response['file_list'] else None

    except BadRequest as e:
        logger.warn("[WARNING] Received bad request - couldn't load JSON.")
        file_manifest = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }
    except Exception as e:
        logger.error("[ERROR] File trieving the file manifest for Cohort {}:".format(str(cohort_id)))
        logger.exception(e)

    return file_manifest


def get_cohort_info(cohort_id, get_barcodes=False):
    cohort = None
    try:
        cohort_obj = Cohort.objects.get(id=cohort_id)
        cohort = {
            'id': cohort_obj.id,
            'name': cohort_obj.name,
            'case_count': cohort_obj.case_size(),
            'sample_count': cohort_obj.sample_size(),
            'programs': cohort_obj.get_program_names(),
            'filters': cohort_obj.get_current_filters(True)
        }

        if get_barcodes:
            cohort['barcodes'] = get_sample_case_list_bq(cohort_id)

    except ObjectDoesNotExist as e:
        logger.warn("Cohort with ID {} was not found!".format(str(cohort_id)))
    except Exception as e:
        logger.exception(e)

    return cohort


def get_cohorts(user_email):

    cohort_list = None

    try:
        user = Django_User.objects.get(email=user_email)
        cohort_perms = Cohort_Perms.objects.filter(user_id=user.id, cohort__active=1)
        cohort_list = []
        for cohort_perm in cohort_perms:
            cohort_list.append({
                'id': cohort_perm.cohort.id,
                'name': cohort_perm.cohort.name,
                'permission': cohort_perm.perm,
                'filters': cohort_perm.cohort.get_current_filters(True)
            })

    except ObjectDoesNotExist as e:
        logger.info("No cohorts found for user {}!".format(user_email))

    return cohort_list


def get_cohort_preview():

    preview = None

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
                result = requests.post("{}/{}".format(DJANGO_URI, 'cohort/preview'),
                            json = request_data,
                            params = params)
            except:
                if result.status_code != 200:
                   raise Exception("oops!")
            #response = result.json()
            return result

#           cohort_counts = get_sample_case_list_bq(None, request_data['filters'])
#
#             if cohort_counts:
#                 for prog in cohort_counts:
#                     if cohort_counts[prog]['case_count'] <= 0:
#                         cohort_counts[prog]['message'] = "No cases or samples found which meet the filter criteria for this program."
#                     cohort_counts[prog]['provided_filters'] = request_data['filters'][prog]

    except BadRequest as e:
        logger.warn("[WARNING] Received bad request - couldn't load JSON.")
        cohort_counts = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }
    except ValidationError as e:
        logger.warn('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        cohort_counts = {
            'message': 'Filters were improperly formatted.'
        }
    except Exception as e:
        logger.exception(e)

    return cohort


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

        if 'filters' not in request_data:
            cohort_info = {
                'message': 'Filters were not provided; at least one filter must be provided for a cohort to be valid.' +
                       ' The cohort was not made.',
            }
            return cohort_info

        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match = blacklist.search(str(request_data['name']))

        if not match and 'desc' in request_data:
            match = blacklist.search(str(request_data['desc']))

        if match:
            cohort_info = {
                'message': 'Your cohort\'s name or description contains invalid characters; please edit them and resubmit. ' +
                    '[Saw {}]'.format(str(match)),
            }

        else:
            result = make_cohort(user, **request_data)

            if 'message' in result:
                cohort_info = result
            else:
                cohort_info = get_cohort_info(result['cohort_id'])

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


def edit_cohort(cohort_id, user, delete=False):
    match = None

    try:
        if delete:
            cohort = Cohort.objects.get(id=cohort_id)
            cohort.active = False
            cohort.save()
            cohort_info = {
                'notes': 'Cohort {} (\'{}\') has been deleted.'.format(cohort_id, cohort.name),
                'data': {'filters': cohort.get_current_filters(unformatted=True)},
            }
        else:
            request_data = request.get_json()
            if len(request_data.keys()):
                schema_validate(request_data, COHORT_FILTER_SCHEMA)

            if 'name' in request_data:
                blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
                match = blacklist.search(str(request_data['name']))

            if match:
                cohort_info = {
                    'message': 'Your cohort\'s name or description contains invalid characters; please edit them and resubmit. ' +
                               '[Saw {}]'.format(str(match)),
                }
            else:
                result = make_cohort(user, source_id=cohort_id, **request_data)
                if 'message' in result:
                    cohort_info = result
                else:
                    cohort_info = get_cohort_info(result['cohort_id'])


    except BadRequest as e:
        logger.warn("[WARNING] Received bad request - couldn't load JSON.")
        cohort_info = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }

    except ObjectDoesNotExist as e:
        logger.error("[ERROR] During {} for cohort ID {}:".format(request.method,str(cohort_id)))
        logger.error("Couldn't find a cohort with that ID!")

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