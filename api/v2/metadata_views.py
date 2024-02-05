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

import requests

from flask import request
from .auth import get_auth
from .version_config import API_VERSION
from .schemas.filters import COHORT_FILTERS_SCHEMA
from python_settings import settings
logger = logging.getLogger(settings.LOGGER_NAME)
BLACKLIST_RE = settings.BLACKLIST_RE

integer_continuous_numerics = (
    'age_at_diagnosis',
    'max_TotalPixelMatrixColumns',
    'max_TotalPixelMatrixRows',
    'min_PixelSpacing'
)

def get_versions():
    auth = get_auth()
    logger.debug("BASE_URL={}".format(settings.BASE_URL))

    response = requests.get(f"{settings.BASE_URL}/collections/api/{API_VERSION}/versions/", headers=auth)
    try:
        if response.status_code != 200:
            logger.error("[ERROR] Error code in response from web app: {}".format(response.status_code))
            logger.error("[ERROR] Request: {}".format(settings.BASE_URL, 'collections/api/versions/'))
            logger.error("[ERROR] auth: {}".format(auth))
            logger.error("[ERROR] Request headers: {}".format(response.request.headers))
            logger.error("[ERROR] Content: {}".format(response.content))
            return dict(
                message="Encountered an error while retrieving the versions list: {}".format(response.content),
                code=response.status_code
            )
        info = response.json()

    except Exception as e:
        logger.error("[ERROR] No content in response from web app")
        logger.error("[ERROR] status_code: {}".format(response.status_code))
        logger.exception(e)
        logger.error("[ERROR] Response dictionary: %s", response.__dict__)

        return dict(
            message="Encountered an error while retrieving the versions list.",
            code=response.status_code
        )
    return info




def get_collections():
    auth = get_auth()
    response = requests.get(f'{settings.BASE_URL}/collections/api/{API_VERSION}/',
                            headers=auth)
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
    info['collections'] = sorted(info['collections'], key = lambda id: id['collection_id'])
    return info


def get_analysis_results():
    auth = get_auth()
    response = requests.get(f"{settings.BASE_URL}/collections/api/{API_VERSION}/analysis_results/",
                             headers=auth)
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

def get_filters():
    auth = get_auth()
    response = requests.get(f"{settings.BASE_URL}/collections/api/{API_VERSION}/attributes/",
                            headers=auth)
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
        for data_source in info["data_sources"]:
            for filter in data_source['filters']:
                if filter["data_type"] =="Continuous Numeric":
                    # filter_data = COHORT_FILTERS_SCHEMA["properties"][filter["name"]]
                    filter["data_type"] = "Ranged Integer" if filter["name"].rsplit('_',1)[0] in integer_continuous_numerics else "Ranged Number"

    except Exception as e:
        logger.error("[ERROR] No content in response from web app")
        logger.error("[ERROR] status_code: {}".format(response.status_code))
        logger.exception(e)
        return dict(
            message="Encountered an error while retrieving the attributes list.",
            code=response.status_code
        )
    return info

def get_fields(version):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    auth = get_auth()
    match = blacklist.search(str(version))
    if match:
        result = dict(
            message=f"Version '{version}' contains invalid characters; please edit and resubmit." ,
            code=400
        )
        return result
    if not version:
        result = dict(
            message=f"No version was provided",
            code=400
        )
        return result
    response = requests.get(f"{settings.BASE_URL}/collections/api/{API_VERSION}/fields/{version}",
                            headers=auth)
    try:
        info = response.json()
        if response.status_code != 200:
            logger.error("[ERROR] Error code in response from web app: {}".format(response.status_code))
            logger.error("[ERROR] auth: {}".format(auth))
            logger.error("[ERROR] Request headers: {}".format(response.request.headers))
            logger.error("[ERROR] Content: {}".format(response.content))
            return dict(
                message="Encountered an error while retrieving the fields list: {}".format(response.content),
                code=response.status_code
            )
    except Exception as e:
        logger.error("[ERROR] No content in response from web app")
        logger.error("[ERROR] status_code: {}".format(response.status_code))
        logger.exception(e)
        return dict(
            message="Encountered an error while retrieving the fields list.",
            code=response.status_code
        )
    return info

