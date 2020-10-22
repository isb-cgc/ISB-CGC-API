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
from flask import jsonify, request, render_template

from python_settings import settings

from . main_views import get_privacy, get_help
from flask import Blueprint

main_bp = Blueprint('main_bp', __name__, url_prefix='/{}'.format(settings.API_VERSION))

logger = logging.getLogger(settings.LOGGER_NAME)

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'


@main_bp.route('/about/', methods=['GET'], strict_slashes=False)
def about():
    """Base response"""
    response = jsonify({
        'code': 200,
        'message': 'Welcome to the NCI IDC API, Version {}'.format(settings.API_VERSION[1:]),
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, settings.API_VERSION) +
             'Documentation available at <https://https://app.gitbook.com/login/imagingdatacommons/idc-user-guide>'
    })
    response.status_code = 200
    return response


# Swagger UI
@main_bp.route('/swagger/', methods=['GET'], strict_slashes=False)
def swagger():
    return render_template('swagger/index.html')


@main_bp.route('/oauth2callback/', strict_slashes=False)
def oauth2callback():
    return render_template('swagger/oauth2-redirect.html')
