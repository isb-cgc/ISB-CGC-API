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
from werkzeug.exceptions import BadRequest

from django.contrib.auth.models import User as Django_User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings

from cohorts.models import Cohort_Perms, Cohort
from cohorts.file_helpers import cohort_files
from cohorts.utils import create_cohort as make_cohort, delete_cohort, get_cohort_cases, get_cohort_files
from projects.models import Program, DataSource, Attribute

from jsonschema import validate as schema_validate, ValidationError
from schemas.cohort_filter_schema import COHORT_FILTER_SCHEMA

BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(__name__)


def convert_api_filters(filter_obj, prog_by_attr=False, attr_to_id=False):
    progs = Program.objects.filter(name__in=filter_obj.keys())
    id_map = progs.name_id_map()
    if prog_by_attr:
        filters = {
            "{}:{}".format(id_map[prog], attr): vals for prog, attrs in filter_obj.items() for attr, vals in
            attrs.items()
        }
    else:
        filters = {
            id_map[prog]: prog_filters for prog, prog_filters in filter_obj.items()
        }

        if attr_to_id:
            filters_by_id = {}
            for prog, attr_filters in filters.items():
                stripped_attrs = {}
                for api_attr in attr_filters.keys():
                    stripped_attr = api_attr if (not '_' in api_attr) else api_attr if not api_attr.rsplit('_', 1)[1] in ['gt', 'gte', 'ebtwe', 'ebtw', 'btwe', 'btw', 'lte', 'lt', 'eq'] else api_attr.rsplit('_', 1)[0]
                    stripped_attrs[stripped_attr] = api_attr
                attrs = Attribute.objects.filter(name__in=stripped_attrs.keys())
                filters_by_id[prog] = {x.id: {'values': attr_filters[stripped_attrs[x.name]]} for x in attrs}
            filters = filters_by_id

    return filters


# Requires login
def get_file_manifest(cohort_id, user):
    file_manifest = None
    inc_filters = {}

    try:
        params = {
        }

        request_data = request.get_json()

        param_set = {
            'offset': {'default': 0, 'type': int, 'name': 'offset'},
            'page': {'default': 1, 'type': int, 'name': 'page'},
            'fetch_count': {'default': 5000, 'type': int, 'name': 'fetch_count'}
        }

        for param, parameter in param_set.items():
            default = parameter['default']
            param_type = parameter['type']
            name = parameter['name']
            params[name] = request_data[param] if (request_data and param in request_data) else request.args.get(
                param, default=default, type=param_type
            ) if param in request.args else default

            if request_data:
                inc_filters = {
                    filter: request_data[filter]
                    for filter in request_data.keys()
                    if filter not in list(param_set.keys())
                }
        file_manifest = {}
        if params['fetch_count'] > settings.MAX_FILE_LIST_REQUEST:
            params['fetch_count'] = min(settings.MAX_FILE_LIST_REQUEST, params['fetch_count'])
            file_manifest['warning'] = "You have requested too many records. Please note the maximum number that may be retrieved in a single operation is 5000."

        result = get_cohort_files(cohort_id, inc_filters=inc_filters, **params)
        file_manifest.update(result)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        file_manifest = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }
    except Exception as e:
        logger.error("[ERROR] While retrieving the file manifest for Cohort {}:".format(str(cohort_id)))
        logger.exception(e)

    return file_manifest


# Requires login
def get_cohort_info(cohort_id, user, get_barcodes=False):
    cohort = None
    cohort_obj = None
    try:
        cohort_obj = Cohort.objects.get(id=cohort_id)
        Cohort_Perms.objects.get(cohort=cohort_obj, user=user, perm=Cohort_Perms.OWNER)
        cohort = {
            'id': cohort_obj.id,
            'name': cohort_obj.name,
            'case_count': cohort_obj.case_count,
            'sample_count': cohort_obj.sample_count,
            'programs': list(cohort_obj.get_program_names()),
            'filters': cohort_obj.get_filters_as_dict_simple()
        }

        if get_barcodes:
            cohort['barcodes'] = get_cohort_cases(cohort_id, source=DataSource.BIGQUERY)

    except ObjectDoesNotExist as e:
        if not cohort_obj:
            logger.warning("Cohort with ID {} was not found!".format(str(cohort_id)))
        else:
            logger.error("User {} do not have access to cohort ID {}!".format(user.email if user else "Unknown", str(cohort_id)))
    except Exception as e:
        logger.exception(e)

    return cohort


# Requires login
def get_cohorts(user_email):

    cohort_list = None

    try:
        user = Django_User.objects.get(email=user_email)
        cohort_perms = Cohort_Perms.objects.select_related('cohort').filter(user=user, cohort__active=1)
        logger.info("[STATUS] cohort perms: {}".format(cohort_perms))
        cohort_list = []
        for cohort_perm in cohort_perms:
            cohort_list.append({
                'id': cohort_perm.cohort.id,
                'name': cohort_perm.cohort.name,
                'permission': cohort_perm.perm,
                'filters': cohort_perm.cohort.get_filters_for_ui()
            })

    except Exception as e:
        logger.error("[ERROR] While retrieving cohorts for {}:".format(user_email))
        logger.exception(e)

    return cohort_list


# Preview method for a cohort, or to get a cohort's case listing; does not require login as it is filter-based
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
            filters = convert_api_filters(request_data['filters'], prog_by_attr=True)
            cohort_counts = get_cohort_cases(None, filters, True, source=DataSource.BIGQUERY)

            if cohort_counts:
                for prog in cohort_counts:
                    if cohort_counts[prog]['case_count'] <= 0:
                        cohort_counts[prog]['message'] = "No cases or samples found which meet the filter criteria for this program."
                    cohort_counts[prog]['provided_filters'] = request_data['filters'][prog]

    except BadRequest as e:
        logger.error("[WARNING] Received bad request - couldn't load JSON.")
        cohort_counts = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }
    except ValidationError as e:
        logger.error('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        cohort_counts = {
            'message': 'Filters were improperly formatted.'
        }
    except Exception as e:
        logger.exception(e)

    return cohort_counts


# Requires login
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

        if request_data.get('description', None):
            request_data['desc'] = request_data.pop('description')

        request_data['filters'] = convert_api_filters(request_data['filters'], attr_to_id=True)

        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match_name = blacklist.search(str(request_data.get('name', '')))
        match_desc = blacklist.search(str(request_data.get('description', '')))

        if match_name or match_desc:
            matches = [x for x in [match_name.group() if match_name else None, match_desc.group() if match_name else None]
                   if x is not None]
            cohort_info = {
                'message': 'Your cohort\'s name or description contains invalid characters; please edit them and resubmit. ' +
                       '[Saw {}]'.format("; ".join(matches)),
            }
        else:
            case_insensitive = request_data['case_insensitive'] if (request_data and 'case_insensitive' in request_data) else request.args.get('case_insensitive', default="True", type=str) if 'case_insensitive' in request.args else "True"
            request_data.pop('case_insensitive', None)
            request_data['case_insens'] = bool(case_insensitive == 'True')

            result = make_cohort(user, **request_data)

            if 'message' in result:
                cohort_info = result
            else:
                cohort_info = get_cohort_info(result['cohort_id'], user)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        cohort_info = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }

    except ValidationError as e:
        logger.warning("[WARNING] Cohort information rejected for improper formatting: {}".format(e))
        cohort_info = {
            'message': 'Cohort information was improperly formatted - cohort not edited.',
        }

    return cohort_info


# Requires login
def edit_cohort(cohort_id, user, delete=False):
    try:
        if delete:
            cohort_info = delete_cohort(user, cohort_id)
        else:
            request_data = request.get_json()
            if len(request_data.keys()):
                schema_validate(request_data, COHORT_FILTER_SCHEMA)

            if 'name' in request_data or 'description' in request_data:
                blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
                match_name = blacklist.search(str(request_data.get('name','')))
                match_desc = blacklist.search(str(request_data.get('description', '')))

            if match_name or match_desc:
                matches = [x for x in [match_name.group() if match_name else None, match_desc.group() if match_name else None] if x is not None]
                cohort_info = {
                    'message': 'Your cohort\'s name or description contains invalid characters; please edit them and resubmit. ' +
                               '[Saw {}]'.format("; ".join(matches)),
                }
            else:
                if request_data.get('filters', None):
                    request_data.pop('filters', None)
                    logger.warning("[WARNING] Saw filters provided for a cohort edit--filters cannot be changed!")
                result = make_cohort(user, source_id=cohort_id, **request_data)
                if 'message' in result:
                    cohort_info = result
                else:
                    cohort_info = get_cohort_info(result['cohort_id'], user)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        cohort_info = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }

    except ValidationError as e:
        logger.warning("[WARNING] Cohort information rejected for improper formatting: {}".format(e))
        cohort_info = {
            'message': 'Cohort information was improperly formatted - cohort not edited.',
        }

    return cohort_info
