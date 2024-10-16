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
from auth import validate_user, UserValidationException
from file_views import get_file_paths, get_signed_uris
from api_logging import *

logger = logging.getLogger(__name__)


@app.route('/v4/files/paths/<file_uuid>/', methods=['GET'], strict_slashes=False)
def file_path(file_uuid):
    resp_obj = None
    code = None

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))

    try:
        file_paths = get_file_paths(file_uuid)

        if file_paths:
            if 'message' in file_paths:
                resp_obj = file_paths
                code = 400
                if 'not_found' in file_paths:
                    code = 404
            else:
                resp_obj = {
                    'data': file_paths
                }
                code = 200
        else:
            resp_obj = {
                'message': 'Encountered an error while retrieving file paths.'
            }
            code = 500

    except Exception as e:
        logger.exception(e)
        resp_obj = {
            'message': 'Encountered an error while retrieving file paths.'
        }
        code = 500
    finally:
        close_old_connections()

    resp_obj['code'] = code
    response = jsonify(resp_obj)
    response.status_code = code

    return response


@app.route('/v4/files/paths/', methods=['POST'], strict_slashes=False)
def file_path_list():

    response_obj = None

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))

    try:
        file_paths = get_file_paths()

        if file_paths:
            # Presence of a message means something went wrong with our request
            if 'message' in file_paths:
                response_obj = file_paths
                code = 400
                if 'not_found' in file_paths:
                    code = 404
            else:
                response_obj = {
                    'data': file_paths
                }
                code = 200

        else:
            response_obj = {
                'message': "Error while attempting to retrieve file manifest for cohort {}.".format(str(cohort_id))
            }
            code = 500

    except Exception as e:
        logger.exception(e)
        response_obj = {
            'message': 'Encountered an error while attempting to retrieve file paths for these file UUIDs.'
        }
        code = 500
    finally:
        close_old_connections()

    response_obj['code'] = code
    response = jsonify(response_obj)
    response.status_code = code
        
    return response
