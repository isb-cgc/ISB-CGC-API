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
from flask import jsonify, request
from apiv4 import app
from django.conf import settings
from django.db import close_old_connections
from sample_case_views import get_sample_metadata, get_case_metadata
from auth import validate_user, UserValidationException

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/apiv4/samples/<sample_barcode>/', methods=['GET'], strict_slashes=False)
def sample_metadata(sample_barcode):
    
    response = None

    try:

        metadata = get_sample_metadata([sample_barcode])

        if metadata and len(metadata['samples']):
            response = jsonify({
                'code': 200,
                'data': metadata['samples'][0]
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 404,
                'message': "Sample barcode {} was not found.".format(sample_barcode)})
            response.status_code = 404
    except Exception as e:
        logger.error("[ERROR] While fetching sample metadata:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving sample metadata for sample barcode {}.'.format(sample_barcode)
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response


@app.route('/apiv4/cases/<case_barcode>/', methods=['GET'], strict_slashes=False)
def case_metadata(case_barcode):

    response = None

    try:
        metadata = get_case_metadata([case_barcode])

        if metadata and len(metadata['cases']):
            response = jsonify({
                'code': 200,
                'data': metadata['cases'][0]
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 404,
                'message': "Case barcode {} was not found.".format(case_barcode)})
            response.status_code = 404
    except Exception as e:
        logger.error("[ERROR] While fetching sample metadata:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving sample metadata for {}.'.format(case_barcode)
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response


@app.route('/apiv4/samples/', methods=['POST'], strict_slashes=False)
def sample_metadata_list():

    response = None

    try:
        request_data = request.get_json()

        metadata = get_sample_metadata(request_data['sample_barcodes'])

        if metadata:
            response = jsonify({
                'code': 200,
                'data': metadata
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 404,
                'message': "Unable to retrieve case metadata for these barcodes: {}".format(str(request_data['sample_barcodes']))
            })
            response.status_code = 404
    except Exception as e:
        logger.error("[ERROR] While fetching sample metadata:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving sample metadata for these barcodes: {}.'.format(str(request_data['sample_barcodes']))
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response


@app.route('/apiv4/cases/', methods=['POST'], strict_slashes=False)
def case_metadata_list():

    response = None
    
    try:
        request_data = request.get_json()

        metadata = get_case_metadata(request_data['case_barcodes'])

        if metadata:
            response = jsonify({
                'code': 200,
                'data': metadata
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 404,
                'message': "Unable to retrieve case metadata for these barcodes: {}".format(str(request_data['case_barcodes']))})
            response.status_code = 404
    except Exception as e:
        logger.error("[ERROR] While fetching case metadata:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving sample metadata for these barcodes: {}.'.format(str(request_data['case_barcodes']))
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response
