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

from flask import request
from werkzeug.exceptions import BadRequest

from django.conf import settings
from cohorts.metadata_helpers import get_paths_by_uuid

from auth import UserValidationException

logger = logging.getLogger(__name__)


def get_file_paths(uuid=None):

    result = None
    uuids = None

    try:

        if uuid:
            uuids = [uuid]
        else:
            request_data = request.get_json()
            if 'uuids' in request_data:
                uuids = request_data['uuids']
            
        if not uuids or not len(uuids):
            result = {
                'message': "File UUIDs not provided in data payload."
            }
        else:
            paths, not_found = get_paths_by_uuid(uuids)
            if not len(paths):
                result = {
                    'message': "No file paths were found for the provided UUIDs.",
                    'not_found': uuids
                }
            else:
                result = {
                    'paths': paths
                }
                if len(not_found):
                    result['notes'] = "File paths were not found for all UUIDs. Please see 'uuids_not_found' for a list."
                    result['not_found'] = not_found

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        result = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }

    return result
