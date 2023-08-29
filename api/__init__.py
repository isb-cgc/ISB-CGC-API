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
# import v1
# import v2

import os

from flask import Flask

from python_settings import settings
import settings as api_settings

settings.configure(api_settings)
assert settings.configured


def create_app(test_config=None):
    # create and configure the app
    if settings.IS_DEV:
        app = Flask(__name__, instance_relative_config=True)
    else:
        app = Flask(__name__, instance_relative_config=True, static_folder='api_static')
    Talisman(app, strict_transport_security_max_age=300, content_security_policy={
        'default-src': [
            '\'self\'',
            '*.googleapis.com',
            '*.swagger.io',
            '\'unsafe-inline\'',
            'data:'
        ]
    })

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    '''from main_routes import *
    from cohorts_routes import *
    from program_routes import *
    from file_routes import *
    from query_routes import *
    from user_routes import *'''

    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.setLevel(settings.LOG_LEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s:%(levelname)s [%(filename)s:%(funcName)s:%(lineno)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    from .v1.query_routes import cohort_query_bp
    app.register_blueprint(cohort_query_bp)

    from .v1.main_routes import main_bp # as v1_main_bp
    app.register_blueprint(main_bp)

    from .v1.cohort_routes import cohorts_bp # as v1_cohorts_bp
    app.register_blueprint(cohorts_bp)

    from .v1.user_routes import user_bp # as v1_user_bp
    app.register_blueprint(user_bp)

    from .v1.metadata_routes import metadata_bp # as v1_metadata_bp
    app.register_blueprint(metadata_bp)

    from .v2.query_routes import cohort_query_bp
    app.register_blueprint(cohort_query_bp)

    from .v2.main_routes import main_bp # as v1_main_bp
    app.register_blueprint(main_bp)

    from .v2.cohort_routes import cohorts_bp # as v1_cohorts_bp
    app.register_blueprint(cohorts_bp)

    from .v2.user_routes import user_bp # as v1_user_bp
    app.register_blueprint(user_bp)

    from .v2.metadata_routes import metadata_bp # as v1_metadata_bp
    app.register_blueprint(metadata_bp)

    @app.context_processor
    def utilities():
        def load_spec(version):
            json_spec = ""
            try:
                yaml = ruamel.yaml.YAML(typ='safe')
                logger.debug(os.path.split(os.path.abspath(dirname(__file__)))[0] + f'/openapi-appengine.{version}.yaml')
                with open(os.path.split(os.path.abspath(dirname(__file__)))[0] + f'/openapi-appengine.{version}.yaml') as fpi:
                    data = yaml.load(fpi)
                    del data['paths']['/swagger']
                    del data['paths']['/oauth2callback']
                    # We need to adjust the security definition for use with Swagger UI itself (as opposed to the deployed API)
                    data['securityDefinitions']['google_id_token'] = {
                        'type': 'oauth2',
                        'authorizationUrl': "https://accounts.google.com/o/oauth2/v2/auth",
                        'tokenUrl': 'https://www.googleapis.com/oauth2/v1/token',
                        'flow': 'implicit',
                        'scopes': {"https://www.googleapis.com/auth/userinfo.email": "User email address",
                                   "openid": "For OIDC"},
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
            static_uri= '' if settings.IS_DEV else (settings.STATIC_URL.replace('/static/', '')),
            api_base_uri=settings.BASE_API_URL,
            ouath2_callback_path="{}/oauth2callback".format(settings.API_VERSION),
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8095, debug=True)
