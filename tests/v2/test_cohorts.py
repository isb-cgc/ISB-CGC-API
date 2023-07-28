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
# from settings import API_VERSION
from testing_config import VERSIONS, API_VERSION

from testing_utils import current_version, create_cohort, delete_cohort


# Test filter schema validation
def test_create_cohort_schema_validation(client, app):
    # Create an invalid filter set
    filters = {
        "collection_id": ["tcga_luad", "tcga_kirc"],
        # Undefined attribute
        "Modalityx": ["CT", "MR"],
        "race": ["WHITE"]}

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filters":filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    response = client.post(f'/{API_VERSION}/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    cohortResponse = response.json
    assert cohortResponse['message']=='Modalityx is not a valid filter.'

    # Create an invalid filter set
    filters = {
        "collection_id": ["tcga_luad", "tcga_kirc"],
        # Undefined attribute
        "Modality": [],
        "race": ["WHITE"]}

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filters":filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    response = client.post(f'/{API_VERSION}/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    cohortResponse = response.json
    assert cohortResponse['message']=='''[WARNING] [] is too short

Failed validating \'minItems\' in schema[\'properties\'][\'Modality\']:
    {\'items\': {\'type\': \'string\'}, \'minItems\': 1, \'type\': \'array\'}

On instance[\'Modality\']:
    []'''

    # Create a valid filter set
    filters = {
        "collection_id": ["tcga_luad", "tcga_kirc"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]}

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filterSet":filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    data = json.dumps(cohortSpec)
    # Corrupt the formatting
    data = data.replace('["CT"', '"CT"')

    response = client.post(f'/{API_VERSION}/cohorts', data=data, headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    cohortResponse = response.json
    assert cohortResponse['message']=='[WARNING] 400 Bad Request: Failed to decode JSON object: Expecting \':\' delimiter: line 1 column 140 (char 139)'


# Test basic cohort creation.
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

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    response = client.post(f'/{API_VERSION}/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohortResponse = response.json['cohort_properties']

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


def test_list_cohorts(client,app):
    cohort0 = create_cohort(client)[0]['cohort_id']
    cohort1 = create_cohort(client)[0]['cohort_id']

    # Get the list of cohorts
    response = client.get(f'{API_VERSION}/cohorts')
    assert response.content_type == 'application/json'
    assert response.status_code == 200

    cohorts = response.json['cohorts']
    assert len([cohort for cohort in cohorts if cohort['cohort_id']==int(cohort0)]) == 1
    assert len([cohort for cohort in cohorts if cohort['cohort_id']==int(cohort1)]) == 1

    delete_cohort(client, cohort0)
    delete_cohort(client, cohort1)


def test_delete_a_cohort(client, app):
    # Try deleting a
    # cohort that probably will never exist
    big_id = 2**64
    response = client.delete(f'{API_VERSION}/cohorts/{big_id}')
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == big_id
    assert cohorts[0]['result']['message'] == "A cohort with the ID {} was not found!".format(str(big_id))

    # Create a cohort
    cohort1 = create_cohort(client)[0]['cohort_id']
    # Delete the cohort we just created
    response = client.delete(f'{API_VERSION}/cohorts/{cohort1}')
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert re.sub(r'\(.*\) ',r'',cohorts[0]['result']['notes'])== \
           "Cohort {} has been deleted.".format(str(cohort1))

    # Get the list of cohorts
    response = client.get(f'{API_VERSION}/cohorts')
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len([cohort for cohort in cohorts if cohort['cohort_id']==int(cohort1)]) == 0

    # Try deleting the cohort we just deleted
    response = client.delete(f'{API_VERSION}/cohorts/{cohort1}')
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert cohorts[0]['result']['message'] == "Cohort ID {} was not found - it may already be deleted.".format(str(cohort1))

def test_delete_cohorts(client, app):
    # Create a cohort
    cohort0 = create_cohort(client)[0]['cohort_id']
    cohort1 = create_cohort(client)[0]['cohort_id']

    # Delete the cohorts that we just created
    cohortIDs = {"cohorts": [cohort0, cohort1]}
    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.delete(f'/{API_VERSION}/cohorts', data=json.dumps(cohortIDs), headers=headers)
    assert response.status_code == 200
    cohorts = response.json['cohorts']

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
    response = client.get("{}/".format(f'{API_VERSION}/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200

    cohorts = response.json['cohorts']
    assert len([cohort for cohort in cohorts
                if cohort['cohort_id']==int(cohort0) or cohort['cohort_id']==int(cohort1)]) == 0




