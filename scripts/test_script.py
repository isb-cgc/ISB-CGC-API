'''
Copyright 2019, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import httplib2
import os
import sys
import requests
import datetime
from google.cloud import storage
from oauth2client.file import Storage
import json
import ruamel.yaml

from test_cases import TEST_CASES_BY_PATH

CREDENTIALS_LOC_ENV = 'ISB_CREDENTIALS'
DEFAULT_CREDENTIALS_LOC = os.path.join(os.path.expanduser("~"), '.isb_credentials')

INFO_BY_TIER = {
    'prod': {
        'yaml_path': 'web-app-deployment-files',
        'yaml': 'prod/prod.openapi-appengine.yaml',
        'project': 'isb-cgc',
        'base_uri': 'https://api-dot-isb-cgc.appspot.com'
    },
    'dev': {
        'yaml_path': 'web-app-deployment-files',
        'yaml': 'dev/dev.openapi-appengine.yaml',
        'project': 'isb-cgc',
        'base_uri': 'https://mvm-api-dot-isb-cgc.appspot.com'
    },
    'test': {
        'yaml_path': 'webapp-deployment-files-test',
        'yaml': 'test.openapi-appengine.yaml',
        'project': 'isb-cgc-test',
        'base_uri': 'https://api-dot-isb-cgc-test.appspot.com'
    }
}

# LEAVE THIS EMPTY
# This is for holding POST'd test cases which will then be used for deletions/searches
COHORTS_FOR_TESTS = []

# Tests which rely on results from previous tests and so must be run in a specific order
# should be listed here
TEST_RELIANCE = {
    'cohorts': [
        {'/': ['post', 'get', 'patch']},
        {'file_manifest': ['post', 'get']},
        {'/': ['delete']}
    ]
}

# LEAVE THIS EMPTY
# This is the holding dict into which the test cases will be built based of test case data
# and the desired tier
API_PATHS = {}


def load_api_paths(tier):
    tier_info = INFO_BY_TIER[tier]
    client = storage.Client(project=tier_info['project'])
    bucket = client.get_bucket(tier_info['yaml_path'])
    yaml_blob = Blob(tier_info['yaml'], bucket)
    file_name = "{}.api.yaml".format(tier)
    with open(file_name, "wb") as file_obj:
        yaml_blob.download_to_file(file_obj)

    file_obj.close()

    with open(file_name, 'r') as fpi:
        data = yaml.load(fpi)

        for path in data['paths']:
            API_PATHS[path] = {
                'methods': {}
            }
            for method in data['paths'][path]:
                API_PATHS[path][method] = {
                    'results': None
                }
                if method == 'post' or method == 'patch' or 'parameters' in data['paths'][path][method]:
                    API_PATHS[path][method]['test_data'] = None
                    if path not in TEST_CASES_BY_PATH:
                        print("[WARNING] The following path cannot be tested, because no test data was found but is required: ")
                        print("path: {}\nmethod: {}".format(path, method.upper()))
                    else:
                        API_PATHS[path][method]['test_data'] = TEST_CASES_BY_PATH[path][method]


def run_tests_and_gather_results(tier, test_set):
    for test in test_set:
        try:
            path = test['path']
            uri = "{}{}".format(INFO_BY_TIER[tier]['base_uri'], path)
            for method in API_PATHS[path]:
                test_data = None
                if 'test_data' in API_PATHS[path][method]:
                    if API_PATHS[path][method]['test_data'] is not None:
                        if method == 'get':
                            uri += API_PATHS[path][method]['test_data']
                        else:
                            test_data = API_PATHS[path][method]['test_data']
                    else:
                        API_PATHS[path][method]['results'] = "FAILED - test case data required but not supplied"

                if not API_PATHS[path][method]['results']:
                    # Requests execution
                    # Parse response
                    print("Running test {} [{}]...".format(path, method))
                    result = requests.request(method.upper(), uri, data=test_data)
        except Exception as e:
            print("[ERROR] During test {}:".format(test))
            print(e)
            print("Test may not have completed!")


def prepare_test_set(tier):
    reliant_tests = []
    unreliant_tests = []

    for path in API_PATHS:
        resources = path.split('/apiv4/')[-1].split('/')
        if resource[0] in TEST_RELIANCE:
            resource_tests = list(TEST_RELIANCE[resource].keys())
            
            for path_base in resource_tests:
                for method in resource_tests[path_base]:
                    this_path = '{}{}{}'.format('/apiv4/', resource, path_base)
                    uri = "{}{}{}".format(INFO_BY_TIER[tier]['base_uri'], resource, path_base)
                    test_data = None
                    if 'test_data' in API_PATHS[this_path][method]:
                        if API_PATHS[this_path][method]['test_data'] is not None:
                            if method == 'get':
                                uri += API_PATHS[this_path][method]['test_data']
                            else:
                                test_data = API_PATHS[this_path][method]['test_data']
                        else:
                            API_PATHS[this_path][method]['results'] = "FAILED - test case data required but not supplied"

                    if not API_PATHS[this_path][method]['results']:
                        # Requests execution
                        # Parse response
                        print("Running test {} [{}]...".format(this_path, method))
                        result = requests.request(method.upper(), uri, data=test_data)


def print_test_run_results(tier):
    for path in API_PATHS:
        for method in API_PATHS[path]:
            print("Results of test {} [{}]\n-----------------------".format(path, method))
            if 'test_data' in API_PATHS[path][method] and API_PATHS[path][method]['test_data']:
                print("Test data: {}".format(str(API_PATHS[path][method]['test_data'])))
            print("Result: {}".format(str(API_PATHS[path][method]['results'])))


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
# encrypted ID token, NOT the access_token, to do a request to Google Endpoints API. To this end we load the
# file as JSON and pull the provided encrypted token there.
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

