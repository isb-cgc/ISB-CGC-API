#
# Copyright 2020, Institute for Systems Biology
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

from python_settings import settings
# from settings import API_VERSION
from testing_config import VERSIONS, API_VERSION

def test_about(client, app):
    response = client.get(f'/{API_VERSION}/about')
    assert client.get(f'/{API_VERSION}/about').status_code == 200
    assert 'NCI IDC API' in response.json['message']


def test_oauth2callback(client, app):
    response = client.get(f'/{API_VERSION}/oauth2callback')
    print(response)


def test_user_info(client, app):
    response = client.get(f'/{API_VERSION}/users/account_details')
    assert response.status_code == 200
    user_details = response.json['user_details']

    assert user_details['email'] == settings.DEBUG_API_EMAIL