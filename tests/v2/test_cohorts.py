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

import json
import re
from testing_config import API_URL, get_data, auth_header
from testing_utils import current_version, create_cohort, delete_cohort, _testMode

import requests

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


@_testMode
def test_invalid_keys(client, app):
    filters = {
        "age_at_diagnosis_btw": [65, 75],
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"]
    }

    cohort_def = {"Name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/',
                           data=json.dumps(cohort_def),
                           headers=headers | auth_header)

    assert response.status_code == 400
    assert get_data(response)['message'] == "'Name' is an invalid cohort_def key"

    cohort_def = {"name": "testcohort",
                  "Description": "Test description",
                  "filters": filters}

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/',
                           data=json.dumps(cohort_def),
                           headers=headers | auth_header)

    assert response.status_code == 400
    assert get_data(response)['message'] == "'Description' is an invalid cohort_def key"

    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/',
                            data = json.dumps(cohort_def),
                            headers=headers | auth_header)

    assert response.status_code == 400
    assert get_data(response)['message'] == "'filters' is a required cohort_def key"

    return


# Test basic cohort creation.
@_testMode
def test_create_cohort(client, app):
    # Create a filter set
    filters = {
        "Collection_ID": ["tcga_luad", "tcga_kirc"],
        "Modality": ["cT", "Mr"],
        "RaCe": ["WHITE"],
        "age_at_diagnosis_btw": [1, 100],
    }

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filters":filters}

    mimetype = 'application/json'
    headers = {
        'Accept': mimetype,
        'Content-Type': mimetype
    }

    try:
        response = client.post(f'{API_URL}/cohorts',
               data=json.dumps(cohortSpec), headers=headers | auth_header)
        # response = requests.post(f'{API_URL}/cohorts',
        #        data=json.dumps(cohortSpec), headers=headers | auth_header)


    except Exception as exc:
        print(exc)
    assert response.status_code == 200
    cohortResponse = get_data(response)['cohort_properties']

    assert cohortResponse['name']=="testcohort"
    assert cohortResponse['description']=="Test description"
    # assert len(cohortResponse['filterSet']) == 1
    assert cohortResponse["filterSet"]["idc_data_version"]==current_version(client)
    assert 'race' in cohortResponse['filterSet']['filters'] and \
           cohortResponse['filterSet']['filters']['race'] == ['WHITE']
    assert 'Modality' in cohortResponse['filterSet']['filters']
    assert  set(value.lower() for value in cohortResponse['filterSet']['filters']['Modality']) == \
            set(['ct', 'mr'])
    assert 'collection_id' in cohortResponse['filterSet']['filters']
    assert set(value.lower() for value in cohortResponse['filterSet']['filters']['collection_id']) == \
           set(['tcga_luad', 'tcga_kirc'])

    # Delete the cohort we just created
    delete_cohort(client, cohortResponse['cohort_id'])


@_testMode
def test_list_cohorts(client,app):
    cohort0 = create_cohort(client)[0]['cohort_id']
    cohort1 = create_cohort(client)[0]['cohort_id']

    # Get the list of cohorts
    response = client.get(f'{API_URL}/cohorts',
                          headers=headers | auth_header)
    assert response.status_code == 200

    cohorts = get_data(response)['cohorts']
    assert len([cohort for cohort in cohorts if cohort['cohort_id']==int(cohort0)]) == 1
    assert len([cohort for cohort in cohorts if cohort['cohort_id']==int(cohort1)]) == 1

    delete_cohort(client, cohort0)
    delete_cohort(client, cohort1)


@_testMode
def test_delete_a_cohort(client, app):
    # Try deleting a
    # cohort that probably will never exist
    big_id = 2**64
    response = client.delete(f'{API_URL}/cohorts/{big_id}',
                             headers=headers | auth_header)
    assert response.status_code == 200
    cohorts = get_data(response)['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == big_id
    assert cohorts[0]['result']['message'] == "A cohort with the ID {} was not found!".format(str(big_id))

    # Create a cohort
    cohort1 = create_cohort(client)[0]['cohort_id']
    # Delete the cohort we just created
    response = client.delete(f'{API_URL}/cohorts/{cohort1}',
                             headers=headers | auth_header)
    assert response.status_code == 200
    cohorts = get_data(response)['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert re.sub(r'\(.*\) ',r'',cohorts[0]['result']['notes'])== \
           "Cohort {} has been deleted.".format(str(cohort1))

    # Get the list of cohorts
    response = client.get(f'{API_URL}/cohorts',
                          headers=headers | auth_header)
    assert response.status_code == 200
    cohorts = get_data(response)['cohorts']
    assert len([cohort for cohort in cohorts if cohort['cohort_id']==int(cohort1)]) == 0

    # Try deleting the cohort we just deleted
    response = client.delete(f'{API_URL}/cohorts/{cohort1}',
                             headers=headers | auth_header)
    assert response.status_code == 200
    cohorts = get_data(response)['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert cohorts[0]['result']['message'] == "Cohort ID {} was not found - it may already be deleted.".format(str(cohort1))

@_testMode
def test_delete_cohorts(client, app):
    # Create a cohort
    cohort0 = create_cohort(client)[0]['cohort_id']
    cohort1 = create_cohort(client)[0]['cohort_id']

    # Delete the cohorts that we just created
    cohortIDs = {"cohorts": [cohort0, cohort1]}
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.delete(f'{API_URL}/cohorts',
                data=json.dumps(cohortIDs), headers=headers | auth_header)
    assert response.status_code == 200
    cohorts = get_data(response)['cohorts']

    assert len(cohorts) == 2
    assert cohorts[0]['cohort_id'] == int(cohort0)
    # assert cohorts[0]['result'] == "Cohort ID {} has been deleted.".format(str(cohort1))
    assert re.sub(r'\(.*\) ',r'',cohorts[0]['result']['notes'])== \
           "Cohort {} has been deleted.".format(str(cohort0))

    assert cohorts[1]['cohort_id'] == int(cohort1)
    # assert cohorts[1]['result'] == "Cohort ID {} has been deleted.".format(str(cohort2))
    assert re.sub(r'\(.*\) ',r'',cohorts[1]['result']['notes'])== \
           "Cohort {} has been deleted.".format(str(cohort1))

    # Get the list of cohorts
    response = client.get(f'{API_URL}/cohorts',
                                       headers=headers | auth_header)
    assert response.status_code == 200

    cohorts = get_data(response)['cohorts']
    assert len([cohort for cohort in cohorts
                if cohort['cohort_id']==int(cohort0) or cohort['cohort_id']==int(cohort1)]) == 0

# Delete all cohorts from the DB
# This should normally be commented out
# Useful to clean up the DB, and to speed up testing
@_testMode
def test_delete_all_cohorts(client, app):
    # Get the list of cohorts
    response = client.get(f'{API_URL}/cohorts',
                          headers=headers | auth_header)
    assert response.status_code == 200

    cohorts = get_data(response)['cohorts']
    for cohort in cohorts:
        delete_cohort(client, cohort['cohort_id'])

