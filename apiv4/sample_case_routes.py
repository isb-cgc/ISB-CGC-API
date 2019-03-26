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
from flask import jsonify, request
from apiv4 import app
from django.conf import settings
from sample_case_views import get_full_sample_metadata, get_case_metadata

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/apiv4/samples/<sample_barcode>/', methods=['GET'], strict_slashes=False)
def sample_metadata(sample_barcode):
    
    response = None

    sample_metadata = get_full_sample_metadata(sample_barcode)
    
    if sample_metadata:
        response = jsonify({
            'code': 200,
            'data': sample_metadata
        })
        response.status_code = 200
    else:
        response = jsonify({
            'code': 404,
            'message': "Sample barcode {} was not found.".format(sample_barcode)})
        response.status_code = 404

    return response


@app.route('/apiv4/cases/<case_barcode>/', methods=['GET'], strict_slashes=False)
def case_metadata(case_barcode):
    response = None

    case_metadata = get_case_metadata(case_barcode)

    if case_metadata:
        response = jsonify({
            'code': 200,
            'data': case_metadata
        })
        response.status_code = 200
    else:
        response = jsonify({
            'code': 404,
            'message': "Case barcode {} was not found.".format(case_barcode)})
        response.status_code = 404

    return response


@app.route('/apiv4/samples/', methods=['POST'], strict_slashes=False)
def sample_metadata_list():
    response = None

    sample_metadata = get_full_sample_metadata(sample_barcode)

    if sample_metadata:
        response = jsonify({
            'code': 200,
            'data': sample_metadata
        })
        response.status_code = 200
    else:
        response = jsonify({
            'code': 404,
            'message': "Sample barcode {} was not found.".format(sample_barcode)})
        response.status_code = 404

    return response


@app.route('/apiv4/cases/', methods=['POST'], strict_slashes=False)
def case_metadata_list():
    response = None
    
    request_data = request.get_json()

    case_metadata = get_case_metadata(case_barcode)

    if case_metadata:
        response = jsonify({
            'code': 200,
            'data': case_metadata
        })
        response.status_code = 200
    else:
        response = jsonify({
            'code': 404,
            'message': "Sample barcode {} was not found.".format(case_barcode)})
        response.status_code = 404

    return response
