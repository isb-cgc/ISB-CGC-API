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
from api_logging import st_logger, make_deprecated_msg, log_name, activity_message

logger = logging.getLogger(__name__)

cohorts_bp = Blueprint(f'cohorts_bp_v4', __name__)


@cohorts_bp.route('/cohorts/<int:cohort_id>/', methods=['GET', 'PATCH', 'DELETE'], strict_slashes=False)
def cohort(cohort_id):
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    return make_deprecated_msg()


@cohorts_bp.route('/cohorts/', methods=['GET', 'POST'], strict_slashes=False)
def cohorts():
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    return make_deprecated_msg()


@cohorts_bp.route('/cohorts/<int:cohort_id>/file_manifest/', methods=['POST', 'GET'], strict_slashes=False)
def cohort_file_manifest(cohort_id):
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    return make_deprecated_msg()


@cohorts_bp.route('/cohorts/preview/', methods=['POST'], strict_slashes=False)
def cohort_preview():
    st_logger.write_text_log_entry(log_name, activity_message.format(request.method, request.full_path))
    return make_deprecated_msg()
