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

from accounts.sa_utils import auth_dataset_whitelists_for_user
from accounts.models import AuthorizedDataset
from projects.models import Program
from auth import get_user_acls, UserValidationException

from jsonschema import validate as schema_validate, ValidationError

BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(settings.LOGGER_NAME)


def get_account_details(user):
    accounts_details = None

    try:
        whitelists = get_user_acls(user)

        if whitelists:
            uads = AuthorizedDataset.objects.filter(whitelist_id__in=whitelists)
            accounts_details = {'dataset_access': [{'name': uad.name, 'whitelist_id': uad.whitelist_id} for uad in uads]}

    except UserValidationException as u:
        logger.warn(u)
        accounts_details = {'message': str(u)}

    except Exception as e:
        logger.error("[ERROR] Encountered an error while retrieving user account details:")
        logger.exception(e)
        accounts_details = {'message': "Encountered an error while retrieving account details for {}.".format(user.email)}

    return accounts_details
