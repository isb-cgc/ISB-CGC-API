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

    # try:
    auth = get_auth()
    logger.debug("BASE_URL={}".format(settings.BASE_URL))
    response = requests.get("{}/{}".format(settings.BASE_URL, 'collections/api/versions/'), headers=auth)
    try:
        info = response.json()
        if response.status_code != 200:
            logger.error("[ERROR] Error code in response from web app: {}".format(response.status_code))
            logger.error("[ERROR] auth: {}".format(auth))
            logger.error("[ERROR] Request headers: {}".format(response.request.headers))
            logger.error("[ERROR] Content: {}".format(response.content))
            return dict(
                message="Encountered an error while retrieving the versions list: {}".format(response.content),
                code=response.status_code
            )

    except Exception as e:
        logger.error("[ERROR] No content in response from web app")
        logger.error("[ERROR] status_code: {}".format(response.status_code))
        logger.exception(e)
        return dict(
            message="Encountered an error while retrieving the versions list.",
            code=response.status_code
        )

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

    auth = get_auth()
    response = requests.get("{}/{}/".format(settings.BASE_URL, 'collections/api/attributes'),
                            params=path_params, headers=auth)
    try:
        info = response.json()
        if response.status_code != 200:
            logger.error("[ERROR] Error code in response from web app: {}".format(response.status_code))
            logger.error("[ERROR] auth: {}".format(auth))
            logger.error("[ERROR] Request headers: {}".format(response.request.headers))
            logger.error("[ERROR] Content: {}".format(response.content))
            return dict(
                message="Encountered an error while retrieving the attributes list: {}".format(response.content),
                code=response.status_code
            )

    except Exception as e:
        logger.error("[ERROR] No content in response from web app")
        logger.error("[ERROR] status_code: {}".format(response.status_code))
        logger.exception(e)
        return dict(
            message="Encountered an error while retrieving the attributes list.",
            code=response.status_code
        )

    return info


def get_collections():
    info = None

    path_params = {
        "idc_data_version": "",
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

    # try:
    auth = get_auth()
    response = requests.get("{}/collections/api/".format(settings.BASE_URL),
                            params=path_params, headers=auth)
    try:
        info = response.json()
        if response.status_code != 200:
            logger.error("[ERROR] Error code in response from web app: {}".format(response.status_code))
            logger.error("[ERROR] auth: {}".format(auth))
            logger.error("[ERROR] Request headers: {}".format(response.request.headers))
            logger.error("[ERROR] Content: {}".format(response.content))
            return dict(
                message="Encountered an error while retrieving the collections list: {}".format(response.content),
                code=response.status_code
            )
    except Exception as e:
        logger.error("[ERROR] No content in response from web app")
        logger.error("[ERROR] status_code: {}".format(response.status_code))
        logger.exception(e)
        return dict(
            message="Encountered an error while retrieving the collections list.",
            code=response.status_code
        )

    return info


def get_analysis_results():
    info = None

    path_params = {
        "idc_data_version": "",
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

    # try:
    auth = get_auth()
    response = requests.get("{}/collections/api/analysis_results/".format(settings.BASE_URL),
                            params=path_params, headers=auth)
    try:
        info = response.json()
        if response.status_code != 200:
            logger.error("[ERROR] Error code in response from web app: {}".format(response.status_code))
            logger.error("[ERROR] auth: {}".format(auth))
            logger.error("[ERROR] Request headers: {}".format(response.request.headers))
            logger.error("[ERROR] Content: {}".format(response.content))
            return dict(
                message="Encountered an error while retrieving the analysis results list: {}".format(response.content),
                code=response.status_code
            )
    except Exception as e:
        logger.error("[ERROR] No content in response from web app")
        logger.error("[ERROR] status_code: {}".format(response.status_code))
        logger.exception(e)
        return dict(
            message="Encountered an error while retrieving the analysis results list.",
            code=response.status_code
        )

    return info


