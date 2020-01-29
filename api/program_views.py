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
import os
import requests

from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)

DJANGO_URI = os.getenv('DJANGO_URI')

def get_programs():
    program_info = None

    try:
        program_info = requests.get("{}/{}".format(DJANGO_URI, 'collections/api/public/'))
    except Exception as e:
        logger.exception(e)

    return program_info


def get_collections(program_name):
    collections_info = None

    try:
        collections_info = requests.get("{}/{}/{}/".format(DJANGO_URI, 'collections/api',program_name))
    except Exception as e:
        logger.exception(e)

    return collections_info

def get_collection_info(program_name, collection_name, version):
    collection_info = None

    try:
        collection_info = requests.get("{}/{}/{}/{}/{}".format(DJANGO_URI, 'collections/api',program_name, collection_name, version))
    except Exception as e:
        logger.exception(e)

    return collection_info

