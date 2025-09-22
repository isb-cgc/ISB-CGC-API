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
from flask import jsonify, request, Blueprint
from api_logging import st_logger, log_name, activity_message
from apiv4 import make_deprecated_msg

logger = logging.getLogger(__name__)

program_bp = Blueprint(f'program_bp_v4', __name__, url_prefix="/api")


@program_bp.route('/data/available/', methods=['GET'], strict_slashes=False)
def data(routes=None):
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    return make_deprecated_msg()


@program_bp.route('/data/available/cohorts/', methods=['GET'], strict_slashes=False)
def data_for_cohorts():
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    return make_deprecated_msg()
