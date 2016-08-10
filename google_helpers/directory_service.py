"""

Copyright 2015, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from oauth2client.client import SignedJwtAssertionCredentials
from googleapiclient import discovery
from django.conf import settings
from httplib2 import Http


PEM_FILE = settings.PEM_FILE
CLIENT_EMAIL = settings.CLIENT_EMAIL
GOOGLE_GROUP_API_ADMIN = settings.GOOGLE_GROUP_API_ADMIN

DIRECTORY_SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.group',
    'https://www.googleapis.com/auth/admin.directory.group.member',
    'https://www.googleapis.com/auth/admin.directory.group.member.readonly',
    'https://www.googleapis.com/auth/admin.directory.group.readonly'
]


def get_directory_resource():

    with open(PEM_FILE) as f:
        private_key = f.read()

    credentials = SignedJwtAssertionCredentials(
        CLIENT_EMAIL,
        private_key,
        DIRECTORY_SCOPES,
        sub=GOOGLE_GROUP_API_ADMIN
        )

    http_auth = credentials.authorize(Http())

    service = discovery.build('admin', 'directory_v1', http=http_auth)
    return service, http_auth