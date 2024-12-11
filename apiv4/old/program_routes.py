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

from flask import Blueprint
from . import make_405_response

old_program_bp = Blueprint(f'program_bp_v41', __name__, url_prefix='/{}'.format("v4"))


@old_program_bp.route('/data/available/registration/', methods=['GET'], strict_slashes=False)
def data_for_reg():

    return make_405_response("The 'data/available/registration' path has been deprecated in version 4.2 due to the " +
                             "removal of controlled access data registration at ISB-CGC.")


@old_program_bp.route('/programs/', methods=['GET'], strict_slashes=False)
def programs():

    return make_405_response("The 'programs' path was deprecated in version 4.1 in favor of /data/availabile and "+
                             "subroutes.")
