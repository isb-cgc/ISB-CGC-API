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
from os.path import join, dirname
import requests

from flask import request

from python_settings import settings

logger = logging.getLogger(settings.LOGGER_NAME)

BLACKLIST_RE = settings.BLACKLIST_RE

def get_auth():
    auth = {"Authorization": "APIToken {}".format(settings.API_AUTH_TOKEN)}
    return auth


def get_versions():
    info = None

    try:
        auth = get_auth()
        response = requests.get("{}/{}".format(settings.BASE_URL, 'collections/api/versions/'), headers=auth)
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info


def get_attributes():
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    info = None

    path_params = {
        "idc_data_version": "",
        "data_source": ""
    }

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

    # try:
    #     auth = get_auth()
    #     response = requests.get("{}/{}/".format(settings.BASE_URL, 'collections/api/attributes'),
    #                             params=path_params, headers=auth)
    #     info = response.json()
    # except Exception as e:
    #     logger.exception(e)
    auth = get_auth()
    response = requests.get("{}/{}/".format(settings.BASE_URL, 'collections/api/attributes'),
                            params=path_params, headers=auth)
    info = response.json()

    return info


def get_collections():
    info = None

    path_params = {
        "idc_data_version": "",
        "program_name": "",
    }

    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)

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
        auth = get_auth()
        response = requests.get("{}/collections/api/".format(settings.BASE_URL),
                                params=path_params, headers=auth)
        info = response.json()
    except Exception as e:
        logger.exception(e)

    return info

