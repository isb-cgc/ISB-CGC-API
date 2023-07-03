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
from flask import jsonify
from python_settings import settings
from api.schemas.queryfields import QUERY_FIELDS

from . metadata_views import get_versions, get_filters, get_collections, get_analysis_results

from flask import Blueprint

metadata_bp = Blueprint('metadata_bp', __name__, url_prefix='/{}'.format(settings.API_VERSION))

logger = logging.getLogger(settings.LOGGER_NAME)


@metadata_bp.route('/versions/', methods=['GET'], strict_slashes=False)
def versions():
    """Retrieve a list of IDC versions"""

    response = None

    try:
        results = get_versions()

        if 'message' in results:
            response = jsonify(results)
            response.status_code = results['code']
        else:
            response = jsonify({
                'code': 200,
                **results
            })
            response.status_code = 200
    except Exception as e:
        logger.error("[ERROR] While retrieving IDC versions:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the versions list.'
        })
        response.status_code = 500

    return response


@metadata_bp.route('/collections/', methods=['GET'], strict_slashes=False)
def collections():
    """Retrieve the list of collections in some IDC versions """
    response = None

    try:
        results = get_collections()

        if 'message' in results:
            response = jsonify(results)
            response.status_code = results['code']
        else:
            response = jsonify({
                'code': 200,
                **results
            })
            response.status_code = 200
    except Exception as e:
        logger.error("[ERROR] While retrieving collection information:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the collection list.'
        })
        response.status_code = 500

    return response

@metadata_bp.route('/analysis_results/', methods=['GET'], strict_slashes=False)
def analysis_results():
    """Retrieve the list of analysis results in some IDC versions """
    response = None

    try:
        results = get_analysis_results()

        if 'message' in results:
            response = jsonify(results)
            response.status_code = results['code']
        else:
            response = jsonify({
                'code': 200,
                **results,
            })
            response.status_code = 200
    except Exception as e:
        logger.error("[ERROR] While retrieving analysis results information:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the analysis results list.'
        })
        response.status_code = 500

    return response

@metadata_bp.route('/filters', methods=['GET'], strict_slashes=False)
def filters():
    """Retrieve a list of filters for the current IDC versions"""
    try:
        results = get_filters()

        if 'message' in results:
            response = jsonify(results)
            response.status_code = results['code']
        else:
            response = jsonify({
                'code': 200,
                **results
            })
            response.status_code = 200
    except Exception as e:
        logger.error("[ERROR] While retrieving filters:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving filters.'
        })
        response.status_code = 500

    return response


@metadata_bp.route('/queryFields', methods=['GET'], strict_slashes=False)
def queryFields():
    """Retrieve a list of query fields for the current IDC versions"""
    fields = [field for field in QUERY_FIELDS['properties']['fields']['items']['enum']]
    response = jsonify({
        'code': 200,
        'queryFields': fields
        })
    response.status_code = 200

    return response



