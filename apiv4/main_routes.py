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
import json
from flask import jsonify, request, render_template
from django.conf import settings
from apiv4 import app

logger = logging.getLogger(settings.LOGGER_NAME)

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'


@app.route('/apiv4/', methods=['GET'], strict_slashes=False)
def apiv4():
    """Base response"""
    response = jsonify({
        'code': 200,
        'message': 'Welcome to the ISB-CGC API, Version 4.',
        'documentation': 'SwaggerUI interface available at <{}/swagger/>.'.format(settings.BASE_API_URL) +
             'Documentation available at <https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/Programmatic-API.html>'
    })
    response.status_code = 200
    return response


# Swagger UI
@app.route('/apiv4/swagger/', methods=['GET'], strict_slashes=False)
def swagger():
    return render_template('swagger/index.html')


@app.route('/oauth2callback')
def oauth2callback():
    redirect_uri = settings.BASE_API_URL+"/oauth2callback"
    if 'code' not in flask.request.args:
        auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                '&client_id={}&redirect_uri={}&scope={}').format(settings.API_CLIENT_ID, redirect_uri, SCOPE)
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        data = {'code': auth_code,
            'client_id': API_CLIENT_ID,
            'client_secret': API_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'}
        r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
        flask.session['credentials'] = r.text

    return flask.redirect(flask.url_for('swagger'))


