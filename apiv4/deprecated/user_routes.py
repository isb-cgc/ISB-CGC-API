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
from flask import redirect, url_for
from apiv4 import app

HTTP_301_MOVED_PERMANENTLY = 301

logger = logging.getLogger(settings.LOGGER_NAME)


def external_url_for(for_this):
    return url_for(for_this, _external=True, _scheme='https')


@app.route('/v4/users/gcp/validate/<gcp_id>/', methods=['GET'], strict_slashes=False)
def validate_gcp_old(gcp_id):
    return redirect(external_url_for('validate_gcp', gcp_id=gcp_id), HTTP_301_MOVED_PERMANENTLY)


@app.route('/v4/users/gcp/<gcp_id>/', methods=['DELETE', 'PATCH', 'GET'], strict_slashes=False)
def user_gcp_old(gcp_id):
    return redirect(external_url_for('user_gcp', gcp_id=gcp_id), HTTP_301_MOVED_PERMANENTLY)


@app.route('/v4/users/gcp/', methods=['POST', 'GET'], strict_slashes=False)
def user_gcps_old():
    print(flask.request.environ['wsgi.url_scheme'])
    return redirect(external_url_for('user_gcps'), HTTP_301_MOVED_PERMANENTLY)
