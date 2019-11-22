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
from flask import jsonify, request, render_template, redirect, url_for
from django.conf import settings
from apiv4 import app
from api_logging import *

logger = logging.getLogger(settings.LOGGER_NAME)

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'


@app.route('/v4/about/', methods=['GET'], strict_slashes=False)
def apiv4():
    """Base response"""

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    
    response = jsonify({
        'code': 200,
        'message': 'Welcome to the ISB-CGC API, Version 4.',
        'documentation': 'SwaggerUI interface available at <{}/swagger/>.'.format(settings.BASE_API_URL) +
             'Documentation available at <https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/Programmatic-API.html>'
    })
    response.status_code = 200
    return response


# Swagger UI
@app.route('/v4/swagger/', methods=['GET'], strict_slashes=False)
def swagger():
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    return render_template('swagger/index.html')


@app.route('/v4/oauth2callback/', strict_slashes=False)
def oauth2callback():
    return render_template('swagger/oauth2-redirect.html')

