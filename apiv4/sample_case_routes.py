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
from flask import jsonify, request, Blueprint
from django.db import close_old_connections
from sample_case_views import get_metadata
from api_logging import *

logger = logging.getLogger(__name__)

NODES = ["PDC", "GDC", "IDC"]

cases_bp = Blueprint(f'cases_bp_v4', __name__, url_prefix='/{}'.format("v4"))


@cases_bp.route('/cases/<source>/<identifier>/', methods=['GET'], strict_slashes=False)
def case_metadata(source, identifier):
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))

    try:
        metadata_from = 'program'
        if source in NODES:
            metadata_from = 'node'

        metadata = get_metadata({metadata_from: {source: [identifier]}})

        if metadata:
            if 'message' in metadata:
                resp_obj = metadata
                code = 400
                if 'barcodes_not_found' in metadata:
                    code = 404
            else:
                resp_obj = {
                    'data': metadata
                }
                code = 200
        else:
            resp_obj = {
                'message': 'Encountered an error while retrieving case metadata.'
            }
            code = 500
    except Exception as e:
        logger.error("[ERROR] While fetching case metadata:")
        logger.exception(e)
        resp_obj = {
            'message': 'Encountered an error while retrieving case metadata for {}.'.format(case_barcode)
        }
        code = 500
    finally:
        close_old_connections()
        
    resp_obj['code'] = code
    response = jsonify(resp_obj)
    response.status_code = code

    return response


@cases_bp.route('/cases/', methods=['POST'], strict_slashes=False)
def case_metadata_list():

    resp_obj = None
    code = None

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))

    try:

        request_data = request.get_json()

        if not(request_data.get('program', None) or request_data.get('node', None)):
            resp_obj = {
                'message': 'Please separate your lists by source type ("node" or "program").'
            }
            code = 400
        else:
            metadata = get_metadata(request_data)

            if metadata:
                if 'message' in metadata:
                    resp_obj = metadata
                    code = 400
                    if 'not_found' in metadata:
                        code = 404
                else:
                    resp_obj = {
                        'data': metadata
                    }
                    code = 200
            else:
                resp_obj = {
                    'message': 'Encountered an error while retrieving case metadata.'
                }
                code = 500
    except Exception as e:
        logger.error("[ERROR] While fetching case metadata:")
        logger.exception(e)
        resp_obj = {
            'message': 'Encountered an error while retrieving case metadata.'
        }
        code = 500
    finally:
        close_old_connections()
        
    resp_obj['code'] = code
    response = jsonify(resp_obj)
    response.status_code = code

    return response
