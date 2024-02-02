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
from testing_branch import test_branch
# DEFAULT_STORAGE_FILE = os.path.join(os.path.expanduser("~"), '.idc_credentials')

API_VERSION = 'v2'
VERSION = 17
NUM_COLLECTIONS = 142

# # True to access dev, testing or prod APIs, False to access local API
# test_remote_api = True
#
# # dev, testing or prod to access the corresponding API when test_dev_api is True
# dev_or_testing_or_prod = 'dev'

DEFAULT_STORAGE_FILE = {
    "LOCAL": "",
    "MASTER": os.path.join(os.path.expanduser("~"), '.idc_credentials_master'),
    "TEST": os.path.join(os.path.expanduser("~"), '.idc_credentials_test'),
    "PROD": os.path.join(os.path.expanduser("~"), '.idc_credentials'),
}[test_branch]

dev_api_requester = requests
API_URL = {
    'LOCAL': f'{API_VERSION}',
    "MASTER": f'https://dev-api.canceridc.dev/{API_VERSION}',
    "TEST": f'https://testing-api.canceridc.dev/{API_VERSION}',
    "PROD": f'https://api.imaging.datacommons.cancer.gov/{API_VERSION}'
}[test_branch]

get_data = dev_response.json if test_branch != "LOCAL" else local_resonse.get_json

if test_branch != "LOCAL":
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

