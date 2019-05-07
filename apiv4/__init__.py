"""

Copyright 2019, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import logging
import os
import sys
from flask import Flask, jsonify, request, render_template, url_for as flask_url_for
from flask_cors import cross_origin
from flask_talisman import Talisman

app = Flask(__name__, static_folder='api_static')
Talisman(app, strict_transport_security_max_age=300)

import django
django.setup()
from django.conf import settings

from auth import auth_info
from main_routes import *
from cohorts_routes import *
from program_routes import *
from sample_case_routes import *
from file_routes import *
from user_routes import *

logger = logging.getLogger(settings.LOGGER_NAME)


def url_for(path, **kwargs):
    url = flask_url_for(path, **kwargs)
    if url.startswith("/static"):
        url = url.replace("/static", "", 1)
        return settings.STATIC_URL + url
    return url


# Swagger UI
@app.route('/apiv4/swagger/', methods=['GET'], strict_slashes=False)
def swagger():
    return render_template('swagger/index.html')


# Error handlers
@app.errorhandler(500)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    logging.error('[ERROR] An error occurred while processing the request:')
    logger.exeception(e)
    response = jsonify({
        'code': 500,
        'message': 'Exception: {}'.format(e)
    })
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8090, debug=True)
