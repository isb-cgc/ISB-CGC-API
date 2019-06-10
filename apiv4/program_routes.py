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
from program_views import get_programs

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/apiv4/programs/', methods=['GET'], strict_slashes=False)
def programs():
    """Retrieve the list of programs and builds currently available for cohort creation."""
    response = None
    
    program_info = get_programs()
    
    if program_info:   
        response = jsonify({
            'code': 200,
            'data': program_info
        })
        response.status_code = 200
    else:
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the program list.'
        })
        response.status_code = 500

    return response
