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
from flask import jsonify, request
from apiv4 import app
from django.conf import settings
from django.db import close_old_connections
from sample_case_views import get_metadata
from api_logging import *

logger = logging.getLogger(__name__)


@app.route('/v4/cases/<case_barcode>/', methods=['GET'], strict_slashes=False)
def case_metadata(case_barcode):

    resp_obj = None

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))

    try:
        metadata = get_metadata(case_barcode, 'case')

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


@app.route('/v4/cases/', methods=['POST'], strict_slashes=False)
def case_metadata_list():

    resp_obj = None
    code = None

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))

    try:
        metadata = get_metadata(type='case')

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
            'message': 'Encountered an error while retrieving case metadata.'
        }
        code = 500
    finally:
        close_old_connections()
        
    resp_obj['code'] = code
    response = jsonify(resp_obj)
    response.status_code = code

    return response
