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
from cohorts.metadata_helpers import get_full_case_metadata, get_full_sample_metadata

logger = logging.getLogger(__name__)


def get_metadata(source, identifier=None, type=None):

    result = None
    barcodes = None
    
    try:
        if identifier:
            barcodes = [identifier]
        else:
            request_data = request.get_json()
            if 'barcodes' in request_data:
                barcodes = request_data['barcodes']

        if not barcodes or not len(barcodes):
            result = {
                'message': 'A list of {} barcodes was not found in this request. Please double-check the expected request JSON format.'.format(type)
            }
        else:
            if type == 'sample':
                result = get_full_sample_metadata(barcodes)
            else:
                result = get_full_case_metadata(barcodes)
            if not result or not result['total_found']:
                if not result:
                    result = {}
                else:
                    del result['total_found']
                result['message'] = "No metadata was found for the supplied {} barcodes.".format(type)
            else:
                if 'not_found' in result:
                    result['notes'] = "Some {} barcodes provided were not found. See 'not_found' for a list.".format(type)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        result = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }

    except Exception as e:
        logger.error("[ERROR] While fetching {} metadata: ".format(type))
        logger.exception(e)

    return result

