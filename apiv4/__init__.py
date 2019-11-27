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
import os
from os.path import join, dirname
import sys
import ruamel.yaml
import json
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from flask_talisman import Talisman

app = Flask(__name__, static_folder='api_static')
Talisman(app, strict_transport_security_max_age=300, content_security_policy={
    'default-src': [
        '\'self\'',
        '*.googleapis.com',
        '*.swagger.io',
        '\'unsafe-inline\'',
        'data:'
    ],
    'connect-src': [
        '\'self\'',
        '*.appspot.com'
    ]
})

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


@app.context_processor
def utilities():
    def load_spec():
        json_spec = ""
        try:
            yaml = ruamel.yaml.YAML(typ='safe')
            logger.debug(os.path.split(os.path.abspath(dirname(__file__)))[0] + '/openapi-appengine.yaml')
            with open(os.path.split(os.path.abspath(dirname(__file__)))[0] + '/openapi-appengine.yaml') as fpi:
                data = yaml.load(fpi)
                del data['paths']['/swagger']
                del data['paths']['/oauth2callback']
                # We need to adjust the security definition for use with Swagger UI itself (as opposed to the deployed API)
                data['securityDefinitions']['google_id_token'] = {
                    'type': 'oauth2',
                    'authorizationUrl': "https://accounts.google.com/o/oauth2/v2/auth",
                    'tokenUrl': 'https://www.googleapis.com/oauth2/v4/token',
                    'flow': 'implicit',
                    'scopes': {"https://www.googleapis.com/auth/userinfo.email": "User email address", "openid": "For OIDC"},
                    'x-tokenName': 'id_token'
                }
                # Escape the ' or the JS will be sad
                json_spec = json.dumps(data).replace("'", "\\'")
        except Exception as e:
            logger.error("[ERROR] While reading YAML spec:")
            logger.exception(e)
        return json_spec

    return dict(
        load_spec=load_spec,
        static_uri=(settings.STATIC_URL.replace('/static/', '')),
        api_base_uri=settings.BASE_API_URL,
        ouath2_callback_path="oauth2callback",
        api_client_id=settings.API_CLIENT_ID
    )


# Error handlers
@app.errorhandler(500)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    logging.error('[ERROR] An error occurred while processing the request:')
    logger.exception(e)
    response = jsonify({
        'code': 500,
        'message': 'Exception: {}'.format(e)
    })
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8090, debug=True)
