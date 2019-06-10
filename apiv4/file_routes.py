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
from auth import validate_user, UserValidationException
from file_views import get_file_paths, get_signed_uris

logger = logging.getLogger(settings.LOGGER_NAME)


# @app.route('/apiv4/files/signed_uris/<file_uuid>/', methods=['GET'], strict_slashes=False)
# def signed_uri(file_uuid):
#     response = None
# 
#     request_data = request.get_json()
# 
#     try:
#         user = validate_user(uuids=[file_uuid])
#         signed_uris = get_signed_uris(user, file_uuid)
# 
#         if signed_uris:
#             response = jsonify({
#                 'code': 200,
#                 'data': signed_uris,
#                 'README': ''
#             })
#             response.status_code = 200
#         else:
#             response = jsonify({
#                 'code': 404,
#                 'message': "File UUID {} was not found.".format(file_uuid)})
#             response.status_code = 404
# 
#     except UserValidationException as e:
#         response = jsonify({
#             'code': 403,
#             'message': str(e)
#         })
#         response.status_code = 403
# 
#     except Exception as e:
#         logger.exception(e)
#         response = jsonify({
#             'code': 500,
#             'message': 'Encountered an error while attempting to retrieve signed URIs for file UUID {}.'.format(file_uuid)
#         })
#         response.status_code = 500
# 
#     return response


# @app.route('/apiv4/files/signed_uris/', methods=['POST'], strict_slashes=False)
# def signed_uri_list():
# 
#     response = None
# 
#     request_data = request.get_json()
# 
#     try:
# 
#         if 'uuids' not in request_data:
#             response = jsonify({
#                 'code': 400,
#                 'message': "File UUIDs not provided in data payload."
#             })
#             response.status_code = 400
#         else:
#             user = validate_user()
#             signed_uris = get_signed_uris(user, request_data['uuids'])
# 
#             if signed_uris:
#                 response = jsonify({
#                     'code': 200,
#                     'data': signed_uris,
#                     'README': ''
#                 })
#                 response.status_code = 200
#             else:
#                 response = jsonify({
#                     'code': 404,
#                     'message': "The provided file UUIDs were not found."})
#                 response.status_code = 404
# 
#     except UserValidationException as e:
#         response = jsonify({
#             'code': 403,
#             'message': str(e)
#         })
#         response.status_code = 403
# 
#     except Exception as e:
#         logger.exception(e)
#         response = jsonify({
#             'code': 500,
#             'message': 'Encountered an error while attempting to retrieve signed URIs for these file UUIDs.'
#         })
#         response.status_code = 500
# 
#     return response


@app.route('/apiv4/files/paths/<file_uuid>/', methods=['GET'], strict_slashes=False)
def file_path(file_uuid):
    response = None

    request_data = request.get_json()

    try:
        file_paths = get_file_paths([file_uuid])

        if file_paths:
            response = jsonify({
                'code': 200,
                'data': file_paths,
                'README': ''
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 404,
                'message': "File UUID {} was not found.".format(file_uuid)})
            response.status_code = 404

    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to retrieve the file path for file UUID {}.'.format(file_uuid)
        })
        response.status_code = 500

    return response


@app.route('/apiv4/files/paths/', methods=['POST'], strict_slashes=False)
def file_path_list():

    response = None

    request_data = request.get_json()

    try:

        if 'uuids' not in request_data:
            response = jsonify({
                'code': 400,
                'message': "File UUIDs not provided in data payload."
            })
            response.status_code = 400
        else:
            file_paths = get_file_paths(request_data['uuids'])

            if file_paths:
                response = jsonify({
                    'code': 200,
                    'data': file_paths,
                    'README': ''
                })
                response.status_code = 200
            else:
                response = jsonify({
                    'code': 404,
                    'message': "The provided file UUIDs were not found."})
                response.status_code = 404

    except Exception as e:
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while attempting to retrieve file paths for these file UUIDs.'
        })
        response.status_code = 500

    return response

