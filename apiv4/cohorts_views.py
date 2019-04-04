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
import django
import re

from flask import request

from django.core.signals import request_finished
from django.contrib.auth.models import User as Django_User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings

from cohorts.models import Cohort_Perms, Cohort, Filters
from accounts.sa_utils import auth_dataset_whitelists_for_user
from cohorts.file_helpers import cohort_files
from cohorts.metadata_helpers import get_sample_case_list_bq
from cohorts.utils import create_cohort as make_cohort
from projects.models import Program

from jsonschema import validate as schema_validate, ValidationError
from schemas.cohort_filter_schema import COHORT_FILTER_SCHEMA

BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(settings.LOGGER_NAME)


def validate_user(user_email, cohort_id=None):
    user = None
    
    django.setup()
    try:
        try:
            user = Django_User.objects.get(email=user_email)
        except ObjectDoesNotExist as e:
            logger.warn("User {} does not exist in our system.".format(user_email))
            return {
                'msg': "User {} does not exist in our system.".format(user_email) +
                " Please register with our Web Application first: <https://isb-cgc.appspot.com>"
            }
       
        try:
            if cohort_id:
                Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user.id)
        except ObjectDoesNotExist as e:
            logger.warn("Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e))
            return {'msg': "User {} does not have access to cohort {}".format(user_email, cohort_id)}
        
    except Exception as e:
        logger.exception(e)
        
    return user


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

        if request_data:
            if request_data['offset']:
                params['offset'] = request.get_assigned_value('offset')

            if request_data['fetch_count']:
                params['limit'] = request.get_assigned_value('fetch_count')

            if request_data['genomic_build']:
                params['build'] = request.get_assigned_value('genomic_build').upper()

            inc_filters = {
                filter: request_data[filter]
                for filter in request_data.keys()
                if filter not in ['cohort_id', 'fetch_count', 'offset', 'genomic_build']
            }

        response = cohort_files(cohort_id, user=user, inc_filters=inc_filters, **params)

        file_manifest = response['file_list'] if response and response['file_list'] else None

    except Exception as e:
        logger.exception(e)

    return file_manifest


def get_cohort_info(cohort_id):
    cohort = None
    try:
        cohort_obj = Cohort.objects.get(id=cohort_id)
        cohort = {
            'id': cohort_obj.id,
            'name': cohort_obj.name,
            'case_count': cohort_obj.case_size(),
            'sample_count': cohort_obj.sample_size(),
            'programs': cohort_obj.get_program_names()
        }
    except ObjectDoesNotExist as e:
        logger.warn("Cohort with ID {} was not found!".format(str(cohort_id)))
    except Exception as e:
        logger.exception(e)

    return cohort


def get_cohorts(user_email):

    cohort_list = None

    try:
        user = Django_User.objects.get(email=user_email)
        cohort_perms = Cohort_Perms.objects.filter(user_id=user.id)
        cohort_list = []
        for cohort_perm in cohort_perms:
            cohort_list.append({
                'id': cohort_perm.cohort.id,
                'name': cohort_perm.cohort.name,
                'permission': cohort_perm.perm
            })

    except ObjectDoesNotExist as e:
        logger.info("No cohorts found for user {}".format(user_email))

    return cohort_list


def get_cohort_counts():
    cohort_counts = None

    try:
        request_data = request.get_json()
        schema_validate(request_data, COHORT_FILTER_SCHEMA)

        if 'filters' not in request_data:
            cohort_counts = {
                'msg': 'No filters were provided; ensure that the request body contains a \'filters\' property.'
            }
        else:
            cohort_counts = get_sample_case_list_bq(None, request_data['filters'])

            for prog in cohort_counts:
                if cohort_counts[prog]['case_count'] <= 0:
                    cohort_counts[prog]['msg'] = "No cases or samples found which meet the filter criteria for this program."
                cohort_counts[prog]['provided_filters'] = request_data['filters'][prog]
    except ValidationError as e:
        logger.warn('Filters rejected for improper formatting: {}'.format(e))
        cohort_counts = {
            'msg': 'Filters were improperly formatted.'
        }
    except Exception as e:
        logger.exception(e)
    return cohort_counts


def create_cohort(user):
    cohort_info = None

    try:
        request_data = request.get_json()
        schema_validate(request_data, COHORT_FILTER_SCHEMA)

        if 'name' not in request_data:
            cohort_info = {
                'msg': 'A name was not provided for this cohort. Cohort was not made.'
            }
            return cohort_info

        if 'filters' not in request_data:
            cohort_info = {
                'msg': 'Filters were not provided; at least one filter must be provided for a cohort to be valid.' +
                       ' Cohort was not made.'
            }
            return cohort_info

        name = request_data['name']
        filters = request_data['filters']

        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match = blacklist.search(str(name))
        if match:
            # XSS risk, log and fail this cohort save
            match = blacklist.findall(str(name))
            cohort_info = {
                'msg': 'Your cohort\'s name contains invalid characters; please choose another name. ' +
                    '[Saw {}]'.format(str(match))
            }
        else:
            desc = None
            if 'description' in request_data:
                desc = request_data['description']

            result = make_cohort(user, filters, name, desc)

            if 'msg' in result:
                cohort_infp = result
            else:
                cohort_info = get_cohort_info(cohort_info['cohort_id'])

    except ValidationError as e:
        logger.warn("Filters rejected for improper formatting: {}".format(e))
        cohort_info = {
            'msg': 'Filters were improperly formatted - cohort not created.'
        }

    return cohort_info


def edit_cohort(cohort_id):
    cohort_info = None

    try:
        request_data = request.get_json()
        schema_validate(request_data, COHORT_FILTER_SCHEMA)

        name = request_data['name']
        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match = blacklist.search(str(name))
        if match:
            # XSS risk, log and fail this cohort save
            match = blacklist.findall(str(name))
            cohort_info = {
                'msg': 'Your cohort\'s name contains invalid characters; please choose another name.' +
                    ' [Saw {}]'.format(str(match))
            }
        else:
            logger.warn("Make cohort")
    except ValidationError as e:
        logger.warn("Filters rejected for improper formatting: {}".format(e))
        cohort_info = {
            'msg': 'Filters were improperly formatted - cohort not created.'
        }

    return cohort_info
