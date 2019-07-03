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
import copy
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
TEST_DEPENDENCIES = {
    'cohorts': [
        {'{cohort_id}': [
            {'get': {'cohort_id': {'path': '/apiv4/cohorts/', 'method': 'post'}}},
            {'patch': {'cohort_id': {'path': '/apiv4/cohorts/', 'method': 'post'}}},
        ]},
        {'{cohort_id}/file_manifest': [
            {'post': {'cohort_id': {'path': '/apiv4/cohorts/', 'method': 'post'}}},
            {'get': {'cohort_id': {'path': '/apiv4/cohorts/', 'method': 'post'}}},
        ]}
    ],
    'users': [
        {'gcp/{gcp_id}': [
            {'patch': {'gcp_id': {'path': '/apiv4/users/gcp/', 'method': 'post'}}},
            {'get': {'gcp_id': {'path': '/apiv4/users/gcp/', 'method': 'post'}}},
            {'delete': {'gcp_id': {'path': '/apiv4/users/gcp/', 'method': 'post'}}}
        ]},
    ]
}

# LEAVE THIS EMPTY
# Test results are written out here
TEST_RESULTS = {}


# LEAVE THIS EMPTY
# This is the holding dict into which the test cases will be built based of test case data
# and the desired tier. Structure:

# API_PATHS = {
#     <tier>: {
#         <resource> : {
#             <subpath>: {
#                 'path': <path>
#                 'methods': {
#                     <method>: {
#                         'auth_req': <True/False>,
#                         ['test_data': {}]
#                     }
#                 }
#             }
#         }
#     }, [...]
# }

API_PATHS = {
    'test': {},
    'dev': {},
    'prod': {}
}


def load_api_paths(tier):
    tier_info = INFO_BY_TIER[tier]
    client = storage.Client(project=tier_info['project'])
    bucket = client.get_bucket(tier_info['yaml_path'])
    yaml_blob = bucket.blob(tier_info['yaml'])

    file_name = "{}.api.yaml".format(tier)

    yaml_blob.download_to_filename(file_name)

    with open(file_name, 'r') as fpi:
        yaml = ruamel.yaml.YAML(typ='safe')
        
        data = yaml.load(fpi)

        for path in data['paths']:
            path_split = path.split('/apiv4/')[-1].split('/')

            resource = path_split[0]
            if len(path_split) > 1:
                subpath = "/".join(path_split[1:])
            else:
                subpath = '/'

            if resource not in API_PATHS:
                API_PATHS[resource] = {}

            if subpath not in API_PATHS[resource]:
                API_PATHS[resource][subpath] = {
                    'methods': {},
                    'path': path
                }

            subpath_set = API_PATHS[resource][subpath]

            for method in data['paths'][path]:
                method_set = {}
                if method == 'post' or method == 'patch' or 'parameters' in data['paths'][path][method]:
                    if resource in TEST_DEPENDENCIES:
                        dependent_subpaths = {list(x.keys())[0]: x[y] for x in TEST_DEPENDENCIES[resource] for y in x}
                        if subpath in dependent_subpaths:
                            dependent_methods = {list(y.keys())[0]: y[z] for x in dependent_subpaths for y in dependent_subpaths[x] for z in y}
                            if method in dependent_methods:
                                method_set['test_data'] = {
                                    'dependencies': dependent_methods[method]
                                }
                    if path in TEST_CASES_BY_PATH:
                        if method.upper() in TEST_CASES_BY_PATH[path]:
                            if 'test_data' not in method_set:
                                method_set['test_data'] = {}
                            method_set['test_data']['test_cases'] = TEST_CASES_BY_PATH[path][method.upper()]
                            
                    if 'parameters' in data['paths'][path][method]:
                        if 'test_data' not in method_set:
                            method_set['test_data'] = {}
                        method_set['test_data']['parameters'] = {}
                        for param in data['paths'][path][method]['parameters']:
                            if param['in'] not in method_set['test_data']['parameters']:
                                method_set['test_data']['parameters'][param['in']] = []
                            method_set['test_data']['parameters'][param['in']].append(param['name'])
                method_set['auth_req'] = bool('security' in data['paths'][path][method])
                subpath_set['methods'][method.upper()] = method_set


def run_tests_and_gather_results(tier, test_set, debug_mode=False):
    TEST_RESULTS[tier] = []
    for test in test_set:
        try:
            path = test['path']
            uri = "{}{}".format(INFO_BY_TIER[tier]['base_uri'], path)
            method = test['method']
            payload = None
            test_result = None

            if 'test_data' in test:
                if test['test_data'] is not None:
                    if 'path' in test['test_data']['parameters']:
                        path_params = {x: test['test_data']['values'][x] for x in test['test_data']['parameters']['path']}
                        uri = uri.format(**path_params)

                    if 'query' in test['test_data']['parameters']:
                        query_string = '&'.join(["{}={}".format(x, test['test_data']['values'][x]) for x in test['test_data']['parameters']['query']])
                        uri += "?{}".format(query_string)

                    if 'body' in test['test_data']['parameters']:
                        payload = {x: test['test_data']['values'][x] for x in test['test_data']['parameters']['body']}
                else:
                    test_result = {'result': "FAILED - test case data required but not supplied"}

            if not test_result:
                test_result = {
                    'path': path,
                    'uri': uri,
                    'method': method,
                    'payload': payload
                }

                headers = {'Content-type': 'application/json'} if payload else {'Content-type': 'text/plain'}
                if test['auth_req']:
                    try:
                        id_token = get_id_token()
                        headers['Authorization'] = 'Bearer {}'.format(id_token)
                    except Exception as e:
                        print("[ERROR] While attempting to obtain login credentials: ")
                        print(e)
                        test_result['result'] = "FAILED - Authorization required but no ID token was found."

                if 'result' not in test_result:
                    # Requests execution
                    # Parse response
                    print("Running test {} [{}]...".format(path, method))
                    if debug_mode:
                        print("DEBUG: request: {} <-> {} <-> {} <-> {}".format(method.upper(), uri, payload, headers))
                    else:
                        response = requests.request(method.upper(), uri, headers=headers, json=payload)
                        if response.headers['Content-type'] == 'application/json':
                            test_result['result'] = response.json()
                        else:
                            test_result['result'] = str(response)

            TEST_RESULTS[tier].append(test_result)

        except Exception as e:
            print("[ERROR] During test {}:".format(str(test)))
            print(e)
            print("Test may not have completed!")


def prepare_test_sets(tier):
    reliant_tests = {}
    unreliant_tests = []
    reliant_paths = None

    for resource in API_PATHS:

        # Check to see if this resource has any reliant subpaths
        if resource in TEST_DEPENDENCIES:
            reliant_paths = set([y for x in TEST_DEPENDENCIES[resource] for y in x])

        for subpath in API_PATHS[resource]:
            for method in API_PATHS[resource][subpath]['methods']:
                method_data = API_PATHS[resource][subpath]['methods'][method]
                # Build test
                test_base = {
                    'path': API_PATHS[resource][subpath]['path'],
                    'auth_req': method_data['auth_req'],
                    'method': method.upper()
                }

                tests = []
                if 'test_data' in method_data:
                    if 'dependencies' in method_data:
                        print("method_data: {}".format(str(method_data)))
                    else:
                        for specific_test in method_data['test_data']['test_cases']:
                            test = copy.deepcopy(test_base)
                            test['test_data'] = {
                                'parameters': method_data['test_data']['parameters'],
                                'values': method_data['test_data']['test_cases'][specific_test]
                            }
                            tests.append(test)
                else:
                    tests.append(copy.deepcopy(test_base))

                if reliant_paths and subpath in reliant_paths:
                    reliant_tests["{}/{}".format(resource, subpath if subpath != '/' else '')] = tests
                else:
                    unreliant_tests.extend(tests)

    return reliant_tests, unreliant_tests


def print_test_run_results(tier):
    for test in TEST_RESULTS[tier]:
        if type(test) is str:
            print(test)
        else:
            print("Results of test {} [{}]".format(test['path'], test['method']))
            if 'test_data' in test and test['test_data']:
                print("Test data: {}".format(str(test['test_data'])))
            print("Result: {}".format(str(test['result'])))
            print("-----------------------------------------------------------------------------------------------------")


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
    tier = 'dev'
    load_api_paths(tier)
    print("API paths loaded, ready to prepare tests")
    print("----------------------------------------")
    reliant, unreliant = prepare_test_sets(tier)
    print("Test sets prepared, ready to run tests on {} tier".format(tier))
    print("-------------------------------------------------")

    print("RELIANT TESTS")
    for test in reliant:
        print(test)
    print("-------------------------------------------------")

    run_tests_and_gather_results(tier, reliant, True)

    # print_test_run_results(tier)


# this allows us to call this from command line
if __name__ == '__main__':
    main()

