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

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def get_privacy():
    DJANGO_URI = os.getenv('DJANGO_URI')
    try:
        result = requests.get("{}/{}".format(DJANGO_URI, 'privacy/'))
    except:
        if result.status_code != 200:
           raise Exception("oops!")
    #response = result.json()
    return result

def get_help():
    DJANGO_URI = os.getenv('DJANGO_URI')
    try:
        result = requests.get("{}/{}".format(DJANGO_URI, 'help/'))
    except:
        if result.status_code != 200:
           raise Exception("oops!")
    #response = result.json()
    return result


