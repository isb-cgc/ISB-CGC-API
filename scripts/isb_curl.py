#! /usr/bin/python2.7
'''
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



isb_curl can be called by commandline or used as a library

URL = https://isb-cgc.appspot.com/_ah/api/{API-NAME}/{VERSION}/{ENDPOINT}?{QUERYSTRING-PARAMS}
  e.g. for the "cohorts_list" endpoint:
  https://isb-cgc.appspot.com/_ah/api/cohort_api/v1/cohorts_list


A. Command Line:
   python isb_auth.py # saves the user's credentials to their root directory
   python isb_curl.py URL
   note: if the endpoint takes a resource in the request body, such as the save_cohort endpoint, use the following:
   python isb_curl.py https://isb-cgc.appspot.com/_ah/api/cohort_api/v1/save_cohort?name={YOUR-COHORT-NAME} \
   -d '{"Study": "BRCA"}' -H "Content-Type: application/json"


B. Python:
    import isb_auth
    import isb_curl
    import requests

    url = 'https://isb-cgc.appspot.com/_ah/api/cohort_api/v1/cohorts_list'
    token = isb_curl.get_access_token()
    head = {'Authorization': 'Bearer ' + token}

    # for GET requests
    resp = requests.get(url, headers=head)
    # querystring parameters can be added to either the url itself...
    url += '?cohort_id=1'
    resp = requests.get(url, headers=head)
    # ... or passed in with the params kwarg
    url = 'https://isb-cgc.appspot.com/_ah/api/cohort_api/v1/cohorts_list'
    params = {'cohort_id': 1}
    resp = requests.get(url, headers=head, params=params)

    # if the endpoint takes a resource in the request body, such as the save_cohort endpoint...
    url = https://isb-cgc.appspot.com/_ah/api/cohort_api/v1/save_cohort?name=my-new-cohort'
    head.update({'Content-Type': 'application/json'})
    payload = {"SampleBarcode": "TCGA-02-0001-01C,TCGA-02-0001-10A,TCGA-01-0642-11A"}
    resp = requests.post(url, headers=head, json=payload)

    # if requests version < 2.4.2
    import json
    resp = requests.post(url, headers=head, data=json.dumps(payload))

'''

import httplib2
import os
import sys
from oauth2client.file import Storage
import json

CREDENTIALS_LOC_ENV = 'ISB_CREDENTIALS'
DEFAULT_CREDENTIALS_LOC = os.path.join(os.path.expanduser("~"), '.isb_credentials')


def check(assertion, msg):
    if not assertion:
        error(msg)


def error(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def get_credentials_location():
    credentials_location = os.environ.get(CREDENTIALS_LOC_ENV, DEFAULT_CREDENTIALS_LOC)
    check(credentials_location, 'Couldn\'t locate the credentials file at {} - run isb_auth.py or check the DEFAULT_CREDENTIALS_LOC at the top of this script.'.format(credentials_location))
    return credentials_location


def load_credentials(credentials_location):
    storage = Storage(credentials_location)
    credentials = storage.get()
    check(credentials and not credentials.invalid, 
          'Couldn\'t locate the credentials file at {} - run isb_auth.py or check the DEFAULT_CREDENTIALS_LOC at the top of this script.'.format(credentials_location))
    return credentials


# Although we can use load_credentials to check the expiration (and re-up if needed), we need the
# encrypted ID token, NOT the access_token, to do a request via the ESP. To this end we load the
# file as JSON and pull the provided encrypted token there (it can also be reconstituted).
def get_id_token(credentials_location=get_credentials_location()):
    credentials = load_credentials(credentials_location)
    if credentials.access_token_expired:
        credentials.refresh(httplib2.Http())
    creds_json = open(credentials_location, "r")
    token = json.loads(creds_json.read())
    return token['token_response']['id_token']


def main():
    args = sys.argv[1:]
    check(args, 'usage: isb_curl.py <curl arguments>')
    id_token = get_id_token()
    curl_args = ['curl', '-H', 'Authorization: Bearer ' + id_token] + args
    os.execvp('curl', curl_args)


# this allows us to call this from command line
if __name__ == '__main__':
    main()


