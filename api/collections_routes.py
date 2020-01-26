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
# from api import app
#from . collections_views import get_collection_info, get_collection_field_info
from django.conf import settings
from django.db import close_old_connections

from flask import Blueprint
from flask import g

collections_bp = Blueprint('collections_bp', __name__, url_prefix='/v1')

logger = logging.getLogger(settings.LOGGER_NAME)



@collections_bp.route('/collections/<collection_id>/<version>', methods=['GET'], strict_slashes=False)
def collection(collection_id, version):
    """"Get a list of the available fields for a specific version of a collection."""
    response = None

    try:
        collection_info = get_collection_info(collection_id, version)

        if collection_info:
            response = jsonify({
                'code': 200,
                'data': collection_info
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while retrieving the collection list.'
            })
            response.status_code = 500
    except Exception as e:
        logger.error("[ERROR] While retrieving collection information:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the collection metadata.'
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response

@collections_bp.route('/collections/<collection_id>/<version>/<field_name>', methods=['GET'], strict_slashes=False)
def collection_field(collection_id, version, field_name):
    """"Get metadata for a field in a specific version of a collection."""
    response = None

    try:

        field_info = get_collection_field_info(collection_id, version, field_name)

        if field_info:
            response = jsonify({
                'code': 200,
                'data': field_info
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while retrieving the collection list.'
            })
            response.status_code = 500
    except Exception as e:
        logger.error("[ERROR] While retrieving collection information:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the collection metadata.'
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response
