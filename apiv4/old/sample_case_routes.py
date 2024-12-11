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

RESPONSE_MSG = "/samples/ paths have been deprecated in version 4.2 due to the restructuring of data from multiple " \
            + "nodes and programs, some of which do not provide sample information. Please use the /cases/ path instead."

samples_bp = Blueprint(f'samples_bp_v41', __name__, url_prefix='/{}'.format("v4"))


@samples_bp.route('/samples/', methods=['POST'], strict_slashes=False)
def sample_metadata_list():

    return make_405_response(RESPONSE_MSG)


@samples_bp.route('/samples/<sample_barcode>/', methods=['GET'], strict_slashes=False)
def sample_metadata(sample_barcode):

    return make_405_response(RESPONSE_MSG)
