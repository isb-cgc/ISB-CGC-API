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
from program_views import get_cohort_programs
from api_logging import *

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/v4/data/available/', methods=['GET'], strict_slashes=False)
def data(routes=None):
    """Retrieve the list of all data available via ISB-CGC"""
    response = None
    response_obj = {}
    response_code = None

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    
    try:
        if not routes or 'cohorts' in routes:
            program_info = get_cohort_programs()
            response_obj['programs_for_cohorts'] = program_info if program_info and len(program_info) > 0 else 'None found'

        response_code = 200
    except Exception as e:
        logger.error("[ERROR] While retrieving data availability:")
        logger.exception(e)
        response_obj = {
            'message': 'Encountered an error while retrieving data availability.'
        }
        response_code = 500
    finally:
        close_old_connections()

    response_obj['code'] = response_code
    response = jsonify(response_obj)
    response.status_code = response_code

    return response


@app.route('/v4/data/available/cohorts/', methods=['GET'], strict_slashes=False)
def data_for_cohorts():
    """Retrieve the list of all data available for cohort creation via ISB-CGC"""
    """This is a pass-through call to the primary /data/available view"""
    return data(['cohorts'])
