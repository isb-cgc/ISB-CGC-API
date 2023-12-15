#
# Copyright 2015-2021, Institute for Systems Biology
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

import os
import requests
from werkzeug.wrappers import Response as local_resonse
from requests.models import Response as dev_response
from scripts.idc_auth import get_credentials
from oauth2client.file import Storage
DEFAULT_STORAGE_FILE = os.path.join(os.path.expanduser("~"), '.idc_credentials')

API_VERSION = 'v2'
VERSIONS = 17
NUM_COLLECTIONS = 142

test_dev_api = True
dev_api_requester = requests
API_URL = f'https://dev-api.canceridc.dev/{API_VERSION}' if test_dev_api else f'{API_VERSION}'
get_data = dev_response.json if test_dev_api else local_resonse.get_json

if test_dev_api:
    # storage = Storage(DEFAULT_STORAGE_FILE)
    # credentials = storage.get()
    # if credentials.access_token_expired:
    #     # credentials have expired so use the refresh_tokem
    #     token = credentials.refresh_token
    # else:
    #     # Still good; use the access token
    #     token = credentials.access_token
    storage = Storage(DEFAULT_STORAGE_FILE)
    credentials = get_credentials(storage)
    # token = credentials.access_token
    token = credentials.token_response['id_token']
    auth_header = {"Authorization": f'Bearer {token}'}
else:
    auth_header = {}

