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
from flask import jsonify, request, render_template, redirect, url_for, Blueprint
from django.conf import settings
from api_logging import *

logger = logging.getLogger(__name__)

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'

main_bp = Blueprint(f'main_bp_v4', __name__, url_prefix='/{}'.format("v4"))


@main_bp.route('/about/', methods=['GET'], strict_slashes=False)
def v4api():
    """Base response"""

    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    
    response = jsonify({
        'code': 200,
        'message': 'Welcome to the ISB-CGC API, Version 4.',
        'documentation': 'SwaggerUI interface available at <{}/swagger/>.'.format(settings.BASE_API_URL) +
             'Documentation available at <https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/progAPI-v4/Programmatic-Demo.html>'
    })
    response.status_code = 200
    return response


# Swagger UI
@main_bp.route('/swagger/', methods=['GET'], strict_slashes=False)
def swagger():
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    return render_template('swagger/index.html')


@main_bp.route('/oauth2callback/', strict_slashes=False)
def oauth2callback():
    return render_template('swagger/oauth2-redirect.html')

