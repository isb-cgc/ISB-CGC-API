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

from flask import request

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
            params['offset'] = request_data['offset'] if 'offset' in request_data['offset'] else request.args.get('offset', default=0, type=int) if request.args.has_key('offset') else 0

            if request_data['fetch_count']:
                params['limit'] = request_data['fetch_count'] if 'fetch_count' in request_data['fetch_count'] else request.args.get('fetch_count', default=5000, type=int) if request.args.has_key('fetch_count') else 5000

            if request_data['page']:
                params['page'] = request_data['page'] if 'page' in request_data['page'] else request.args.get('page', default=1, type=int) if request.args.has_key('page') else 1

            if request_data['genomic_build']:
                params['build'] = request_data['genomic_build'] if 'genomic_build' in request_data['genomic_build'] else request.args.get('genomic_build', default="HG19", type=str) if request.args.has_key('genomic_build') else 'HG19'

            inc_filters = {
                filter: request_data[filter]
                for filter in request_data.keys()
                if filter not in ['cohort_id', 'fetch_count', 'offset', 'genomic_build']
            }

        response = cohort_files(cohort_id, user=user, inc_filters=inc_filters, **params)

        file_manifest = response['file_list'] if response and response['file_list'] else None

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
            'programs': cohort_obj.get_program_names()
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
        cohort_perms = Cohort_Perms.objects.filter(user_id=user.id)
        cohort_list = []
        for cohort_perm in cohort_perms:
            cohort_list.append({
                'id': cohort_perm.cohort.id,
                'name': cohort_perm.cohort.name,
                'permission': cohort_perm.perm
            })

    except ObjectDoesNotExist as e:
        logger.info("No cohorts found for user {}!".format(user_email))

    return cohort_list


def get_cohort_counts():

    cohort_counts = None

    try:
        request_data = request.get_json()
        schema_validate(request_data, COHORT_FILTER_SCHEMA)

        if 'filters' not in request_data:
            cohort_counts = {
                'message': 'No filters were provided; ensure that the request body contains a \'filters\' property.'
            }
        else:
            cohort_counts = get_sample_case_list_bq(None, request_data['filters'])

            for prog in cohort_counts:
                if cohort_counts[prog]['case_count'] <= 0:
                    cohort_counts[prog]['message'] = "No cases or samples found which meet the filter criteria for this program."
                cohort_counts[prog]['provided_filters'] = request_data['filters'][prog]
    except ValidationError as e:
        logger.warn('Filters rejected for improper formatting: {}'.format(e))
        cohort_counts = {
            'message': 'Filters were improperly formatted.'
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
                'message': 'A name was not provided for this cohort. The cohort was not made.',
                'code': 400
            }
            return cohort_info

        if 'filters' not in request_data:
            cohort_info = {
                'message': 'Filters were not provided; at least one filter must be provided for a cohort to be valid.' +
                       ' The cohort was not made.',
                'code': 400
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
                'code': 400
            }

        else:
            result = make_cohort(user, **request_data)

            if 'message' in result:
                cohort_info = result
            else:
                cohort_info = get_cohort_info(result['cohort_id'])

    except ValidationError as e:
        logger.warn("[WARNING] Cohort information rejected for improper formatting: {}".format(e))
        cohort_info = {
            'message': 'Cohort information was improperly formatted - cohort not edited.',
            'code': 400
        }

    return cohort_info


def edit_cohort(cohort_id, user, delete=False):
    result = None
    match = None

    try:
        if delete:
            cohort = Cohort.objects.get(id=cohort_id)
            cohort.active = False
            cohort.save()
            result = {
                'message': 'Cohort {} (\'{}\') has been deleted.'.format(cohort_id, cohort.name),
                'data': {'filters': cohort.get_current_filters(unformatted=True)},
                'code': 200
            }
        else:
            request_data = request.get_json()
            if len(request_data.keys()):
                schema_validate(request_data, COHORT_FILTER_SCHEMA)

            if 'name' in request_data:
                blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
                match = blacklist.search(str(request_data['name']))

            if not match and 'desc' in request_data:
                match = blacklist.search(str(request_data['desc']))

            if match:
                result = {
                    'message': 'Your cohort\'s name or description contains invalid characters; please edit them and resubmit. ' +
                               '[Saw {}]'.format(str(match)),
                    'code': 400
                }
            else:
                result = make_cohort(user, source_id=cohort_id, **request_data)

    except ObjectDoesNotExist as e:
        logger.error("[ERROR] During {} for cohort ID {}:".format(request.method,str(cohort_id)))
        logger.error("Couldn't find a cohort with that ID!")
        result = {
            'message': 'Cohort with ID {} not found.'.format(str(cohort_id)),
            'code': 404
        }
    except ValidationError as e:
        logger.warn("[WARNING] Cohort information rejected for improper formatting: {}".format(e))
        result = {
            'message': 'Cohort information was improperly formatted - cohort not edited.',
            'code': 400
        }

    return result
