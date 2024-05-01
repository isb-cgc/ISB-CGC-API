#
# Copyright 2015-2022, Institute for Systems Biology
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

# Authenticates user for accessing the IDC Endpoint APIs.
#
# May be run from the command line or in scripts/ipython.
#
# The oauth2client functionality is called from your application and runs
# through all the steps to obtain credentials. It takes a ``Flow``
# argument and attempts to open an authorization server page in the
# user's default web browser. The server asks the user to grant your
# application access to the user's data. If the user grants access,
# the ``run()`` function returns new credentials. The new credentials
# are also stored in the ``storage`` argument, which updates the file
# associated with the ``Storage`` object.
#
# The resulting credentials file can be copied to any machine from which you want
# to access the API.
#
# 1. Command Line
#    python ./idc_auth.py          saves the user's credentials;
#                       OPTIONAL:
#                          -v       for verbose (returns token!)
#                          -s FILE  sets credentials file [default: ~/.idc_credentials]
#                          -u       URL-only: for use over terminal connections;
#                                   gives user a URL to paste into their browser,
#                                   and asks for an auth code in return
#
# 2. Python
#     import idc_auth
#     credentials = idc_auth.get_credentials()
#
# # optional: to store credentials in a different location
#     from oauth2client.file import Storage
#     import idc_auth
#     import os
#
#     storage_file = os.path.join(os.path.expanduser("~"), "{USER_CREDENTIALS_FILE_NAME}")
#     storage = Storage(storage_file)
#     credentials = get_credentials(storage=storage)
# # Notes:
#
# The script requires version 4.1.3 of the oauth2client module.
#
# In some cases you might not want your credentials written to the local files system. In such a case,
# use /dev/null as the storage_file:
#     from oauth2client.file import Storage
#     import idc_auth
#     import os
#
#     storage_file = "/dev/null"
#     storage = Storage(storage_file)
#     credentials = get_credentials(storage=storage)
#
# The oauth2client module must be run on a machine that is running a browser.

from argparse import ArgumentParser
import os

import httplib2
import pkg_resources
pkg_resources.require("oauth2client==4.1.3")
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.file import Storage
from scripts.idc_auth import get_credentials

VERBOSE = False
CLIENT_ID = '198650116749-jold6g3160renk0nm566m7tguvpdktga.apps.googleusercontent.com'
# Note: This script is for a "public client", where true secrets cannot be stored. The actual security of this OAuth flow
# lies in the PKCE dynamically-generated secret, which this script is using. In this case, this so-called
# "client secret" cannot be considered anything more than an additional piece of the public client ID. It is only
# provided because Google still requires it to be present when an authorization code is exchanged for an access token.
# Do not use this ID/secret pair in any OAuth2 flow that does not use PKCE.
CLIENT_SECRET = 'tQdFIEHMlueJAa0vnKNPfArS'
EMAIL_SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
CLOUD_PLATFORM_SCOPE='https://www.googleapis.com/auth/cloud-platform'
DEFAULT_STORAGE_FILE = os.path.join(os.path.expanduser("~"), '.idc_credentials')
class flags():
    auth_host_name='localhost'
    noauth_local_webserver=False
    auth_host_port=[8080, 8090]
    logging_level='ERROR'
FLAGS = flags()

def maybe_print(msg):
    if VERBOSE:
        print(msg)


def get_credentials(storage=None, flags=FLAGS):
    if storage is None:
        storage = Storage(DEFAULT_STORAGE_FILE)
    credentials = storage.get()
    # if not credentials or credentials.invalid or credentials.access_token_expired:
    if not credentials or credentials.invalid:
        maybe_print('credentials missing/invalid/expired, kicking off OAuth flow')
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, EMAIL_SCOPE, pkce=True)
        credentials = tools.run_flow(flow, storage, flags)
    elif credentials.access_token_expired:
        if credentials.access_token_expired:
            h = httplib2.Http()
            credentials.refresh(h)
    return credentials


def main():
    global VERBOSE
    global CLIENT_ID
    global CLIENT_SECRET
    args = parse_args()
    VERBOSE = args.verbose
    CLIENT_ID = args.client_id
    CLIENT_SECRET = args.client_secret
    maybe_print('--verbose: printing extra information')
    storage = Storage(args.storage_file)
    credentials = get_credentials(storage)
    maybe_print('credentials stored in ' + args.storage_file)
    maybe_print('access_token: ' + credentials.access_token)
    maybe_print('refresh_token: ' + credentials.refresh_token)


def parse_args():
    parser = ArgumentParser()
    # parser.add_argument('--storage_file', '-s', default=DEFAULT_STORAGE_FILE, help='storage file to use for the credentials (default is {})'.format(DEFAULT_STORAGE_FILE))
    parser.add_argument('--storage_file', '-s', default='/Users/BillClifford/.idc_credentials_test', help='storage file to use for the credentials (default is {})'.format(DEFAULT_STORAGE_FILE))
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_false', help='display credentials storage location, access token, and refresh token')
    parser.set_defaults(verbose=False)
    parser.add_argument('--client_id', default=CLIENT_ID)
    parser.add_argument('--client_secret', default=CLIENT_SECRET)
    return parser.parse_args()


if __name__ == '__main__':
    main()