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

from flask import request

from django.core.signals import request_finished
from django.contrib.auth.models import User as Django_User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings

from cohorts.models import Cohort_Perms, Cohort, Filters
from accounts.sa_utils import auth_dataset_whitelists_for_user
from cohorts.file_helpers import cohort_files

logger = logging.getLogger('main_logger')


def validate_user(user_email, cohort_id):
    user = None
    django.setup()
    try:
        user = Django_User.objects.get(email=user_email)
        Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user.id)
    except ObjectDoesNotExist as e:
        logger.warn("Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e))
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
        cohort_obj = Cohorts.objects.get(id=cohort_id)
        cohort = {
            'id': cohort_obj.id,
            'name': cohort_obj.name,
            'case_count': cohort_obj.case_size(),
            'sample_count': cohort_obj.sample_size(),
            'creation_filters': cohort_obj.get_current_filters(),
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
