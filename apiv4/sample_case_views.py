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
from cohorts.metadata_counting import get_full_case_metadata

logger = logging.getLogger(__name__)

NODES = ["PDC", "GDC", "IDC"]


def get_metadata(ids):

    result = None
    
    try:
        for source_type, source_sets in ids.items():
            id_set_type = "{} {}s".format(source_type, "case barcode" if source_type == "program" else "uuid")
            for source, id_set in source_sets.items():
                if not id_set or not len(id_set):
                    result = {
                        'message': 'A list of {} was not found in this request. Please double-check the expected request JSON format.'.format(
                            id_set_type
                        )
                    }
                else:
                    result = get_full_case_metadata(id_set, source_type, source)
                    if not result or not result['total_found']:
                        if not result:
                            result = {}
                        else:
                            del result['total_found']
                        result['message'] = "No metadata was found for the supplied {}.".format(id_set_type)
                    else:
                        if 'not_found' in result:
                            result['notes'] = "Some {} provided were not found. See 'not_found' for a list.".format(id_set_type)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        result = {
            'message': 'The JSON provided in this request appears to be improperly formatted.',
        }

    except Exception as e:
        logger.error("[ERROR] While fetching {} metadata: ".format(type))
        logger.exception(e)

    return result

