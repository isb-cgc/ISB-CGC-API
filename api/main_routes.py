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

from django.conf import settings
from django.db import close_old_connections


from . main_views import get_privacy, get_help
#from api import app

# Configure Blueprint for about
#from flask import (
#    Blueprint, flash, g, redirect, render_template, request, session, url_for
#)

from flask import Blueprint
from flask import g

main_bp = Blueprint('main_bp', __name__, url_prefix='/v1')
#

logger = logging.getLogger(settings.LOGGER_NAME)

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'


#@app.route('/v1/about/', methods=['GET'], strict_slashes=False)
@main_bp.route('/about/', methods=['GET'], strict_slashes=False)
def about():
    """Base response"""
    response = jsonify({
        'code': 200,
        'message': 'Welcome to the NCI IDC API, Version 1.',
        'documentation': 'SwaggerUI interface available at <{}/v1/swagger/>.'.format(settings.BASE_API_URL) +
             'Documentation available at <https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/Programmatic-API.html>'
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


# This will likely be deleted at some point. It's here just to be able to test an API entrypoint that can be
# satisfied by the webapp.
@main_bp.route('/help/', methods=['GET'], strict_slashes=False)
def help():
    try:
        help_info = get_help()

        if help_info:
            response = jsonify({
                'code': 200,
                'data': help_info.text
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while retrieving the help info.'
            })
            response.status_code = 500
    except Exception as e:
        logger.error("[ERROR] While retrieving help information:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the help list.'
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response


