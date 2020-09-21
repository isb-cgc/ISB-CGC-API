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
import re
import os
import requests

from flask import request

from python_settings import settings

logger = logging.getLogger(settings.LOGGER_NAME)

BLACKLIST_RE = settings.BLACKLIST_RE
DJANGO_URI = os.getenv('DJANGO_URI')

def get_versions():
    info = None

    try:
        response = requests.get("{}/{}".format(DJANGO_URI, 'collections/api/versions/'))
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info


def get_programs():
    info = None

    try:
        response = requests.get("{}/{}".format(DJANGO_URI, 'collections/api/programs/'))
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info


def get_data_sources():
    path_params = {
        "idc_version": "",
    }

    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    info = None

    # Get and validate parameters
    for key in request.args.keys():
        match = blacklist.search(str(key))
        if match:
            return dict(
                message="Argument {} contains invalid characters; please edit and resubmit. " +
                        "[Saw {}]".format(str(key, match)),
                code=400
            )
        if key in path_params:
            path_params[key] = request.args.get(key)
        else:
            return dict(
                message="Invalid argument {}".format((key)),
                code=400
            )

    try:
        response = requests.get("{}/{}/".format(DJANGO_URI, 'collections/api/data_sources'),
                                params=path_params)
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info


def get_attributes(data_source):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    info = None

    path_params = {
        "idc_version": "",
    }

    match = blacklist.search(data_source)
    if match:
        return dict(
            message="Data source {} contains invalid characters; please edit and resubmit. " +
                    "[Saw {}]".format(str(data_source, match)),
            code=400
        )
    # Get and validate parameters
    for key in request.args.keys():
        match = blacklist.search(str(key))
        if match:
            return dict(
                message="Argument {} contains invalid characters; please edit and resubmit. " +
                        "[Saw {}]".format(str(key, match)),
                code=400
            )
        if key in path_params:
            path_params[key] = request.args.get(key)
        else:
            return dict(
                message="Invalid argument {}".format((key)),
                code=400
            )

    try:
        response = requests.get("{}/{}/{}/".format(DJANGO_URI, 'collections/api/attributes', data_source),
                                params=path_params)
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info


def get_program_collections(program):
    info = None

    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    match = blacklist.search(str(program))
    if match:
        info = {
            "message": "Your program name contains invalid characters; please edit and resubmit. " +
                       "[Saw {}]".format(str(match)),
            "code": 400,
            "not_found": []
        }

    try:
        response = requests.get("{}/collections/api/programs/{}/".format(DJANGO_URI, program))
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info

def get_collections(idc_version):
    info = None

    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    match = blacklist.search(str(idc_version))
    if match:
        info = {
            "message": "Your idc_version contains invalid characters; please edit and resubmit. " +
                       "[Saw {}]".format(str(match)),
            "code": 400,
            "not_found": []
        }

    try:
        response = requests.get("{}/collections/api/{}/".format(DJANGO_URI, idc_version))
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info


# def get_collection_info(program_name, collection_name):
#     info = None
#
#     request_string = {}
#     for key in request.args.keys():
#         request_string[key] = request.args.get(key)
#     if "attribute_type" not in request_string:
#         info = {
#             "message": "An attribute_type was not specified. Collection details could not be provided.",
#             "code": 400,
#             "not_found": []
#         }
#         return info
#
#     blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
#     match = blacklist.search(str(request_string["attribute_type"]))
#     if not match and "version" in request_string:
#         match = blacklist.search(str(request_string["version"]))
#     if match:
#         info = {
#             "message": "Your collections\'s attribute_type or version contain invalid characters; please edit them and resubmit. " +
#                        "[Saw {}]".format(str(match)),
#             "code": 400,
#             "not_found": []
#         }
#     else:
#         try:
#             response = requests.get("{}/{}/{}/{}/".format(
#                 DJANGO_URI, "collections/api",program_name, collection_name),
#                 params=request_string)
#             info = response.json()
#         except Exception as e:
#             logger.exception(e)
#
#     return info
#
