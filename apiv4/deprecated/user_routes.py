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

from apiv4 import app
from . import make_405_response

RESPONSE_MSG = "The 'gcp' path has been deprecated in version 4.1 in favor of /cloud_projects and subroutes."


@app.route('/v4/users/gcp/validate/<gcp_id>/', methods=['GET'], strict_slashes=False)
def validate_gcp_old(gcp_id):
    return make_405_response(RESPONSE_MSG)


@app.route('/v4/users/gcp/<gcp_id>/', methods=['DELETE', 'PATCH', 'GET'], strict_slashes=False)
def user_gcp_old(gcp_id):
    return make_405_response(RESPONSE_MSG)


@app.route('/v4/users/gcp/', methods=['POST', 'GET'], strict_slashes=False)
def user_gcps_old():
    return make_405_response(RESPONSE_MSG)
