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
from .schemas.filters import COHORT_FILTERS_SCHEMA
from .version_config import API_VERSION
from . metadata_views import get_versions, get_filters, get_collections, get_analysis_results, get_fields
from flask import Blueprint
from google.cloud import bigquery

logger = logging.getLogger(settings.LOGGER_NAME)

metadata_bp = Blueprint(f'metadata_bp_{API_VERSION}', __name__, url_prefix='/{}'.format(API_VERSION))

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
                **results
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
    # """Retrieve a list of filters for the current IDC versions"""
    # "Retrieve a list of query fields for the current IDC versions"
    # filters = [filter for filter in COHORT_FILTERS_SCHEMA['properties']]
    #
    #
    # # response = jsonify({
    # #     'code': 200,
    # #     'queryFields': filters
    # #     })
    # # response.status_code = 200
    # response = jsonify({
    #     'code': 200,
    #     'queryFields': filters
    #     })
    # return response


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

# Get the accepted values of a categorical filter
@metadata_bp.route('/filters/values/<string:filter_id>', methods=['GET'], strict_slashes=False)
def categorical_values(filter_id):
    client = bigquery.Client('idc-dev-etl')

    try:
        results = get_filters()

        if 'message' in results:
            response = jsonify(results)
            response.status_code = results['code']

        for source in results['data_sources']:
            filter = next((filter for filter in source['filters'] if filter['name'].lower() == filter_id.lower()), -1)
            if filter == -1:
                continue
        if filter == -1:
            response = jsonify({
                'code': 500,
                'message': 'Invalid filter ID'
            })
            response.status_code = 500
            return response
        if filter['data_type'] not in ['Categorical String', 'Categorical Number']:
            response = jsonify({
                'code': 500,
                'message': f'Filter data type is {filter["data_type"]} not Categorical String or Categorical Number'
            })
            response.status_code = 500
            return response
        query = f"""
        SELECT DISTINCT {filter['name']}
        FROM `{source['data_source']}`
        ORDER BY {filter['name']}
        """
        try:
            values = [row[filter['name']] for row in client.query(query)]
            response = jsonify({
                'code': 200,
                'values': values
            })
            response.status_code = 200
        except Exception as exc:
            response = jsonify({
                'code': 500,
                'message': f'Internal error obtaining accepted values'
            })
            response.status_code = 500
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
    try:
        results = get_fields()

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
        logger.error("[ERROR] While retrieving queryFields:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving queryFields.'
        })
        response.status_code = 500

    return response


