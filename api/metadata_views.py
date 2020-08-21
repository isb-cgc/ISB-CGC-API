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
        response = requests.get("{}/{}".format(DJANGO_URI, 'collections/api/public/'))
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info


def get_attributes():
    info = None

    try:
        response = requests.get("{}/{}".format(DJANGO_URI, 'collections/api/attributes/'))
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info


def get_collections(program_name):
    info = None

    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    match = blacklist.search(str(program_name))
    if match:
        info = {
            "message": "Your program_name contains invalid characters; please edit and resubmit. " +
                       "[Saw {}]".format(str(match)),
            "code": 400,
            "not_found": []
        }

    try:
        response = requests.get("{}/{}/{}/".format(DJANGO_URI, 'collections/api',program_name))
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info

def get_collection_info(program_name, collection_name):
    info = None

    request_string = {}
    for key in request.args.keys():
        request_string[key] = request.args.get(key)
    if "attribute_type" not in request_string:
        info = {
            "message": "An attribute_type was not specified. Collection details could not be provided.",
            "code": 400,
            "not_found": []
        }
        return info

    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    match = blacklist.search(str(request_string["attribute_type"]))
    if not match and "version" in request_string:
        match = blacklist.search(str(request_string["version"]))
    if match:
        info = {
            "message": "Your collections\'s attribute_type or version contain invalid characters; please edit them and resubmit. " +
                       "[Saw {}]".format(str(match)),
            "code": 400,
            "not_found": []
        }
    else:
        try:
            response = requests.get("{}/{}/{}/{}/".format(
                DJANGO_URI, "collections/api",program_name, collection_name),
                params=request_string)
            info = response.json()
        except Exception as e:
            logger.exception(e)

    return info

