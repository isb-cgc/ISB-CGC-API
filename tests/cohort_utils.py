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

levels = ["collections", "patients", "studies", "series", "instances"]

def pretty_print_cohortObjects(cohortObjects, indent=4):
    print(json.dumps(cohortObjects, sort_keys=True, indent=indent))

# This routine merges results from the /cohorts/{cohort_id} API with previously obtained results.
# It is intended for use when that API is used in a paged manner.
def merge(src, dst, level):
    keys = ["collection_id", "patient_id", "StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID"]
    for src_item in src:
        found = False
        for dst_item in dst:
            # if src_item["id"] == dst_item["id"]:
            if src_item[keys[level]] == dst_item[keys[level]]:
                if not len(levels) == level+1:
                    merge(src_item[levels[level+1]], dst_item[levels[level+1]], level+1)
                found = True
                break
        if not found:
            dst.append(src_item)

 # Utility to create a "standard" cohort for testing
def create_cohort(client):
    # Create a filter set
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"]}}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohortResponse = response.json['cohort_properties']

    return cohortResponse

# Create a cohort with filter as expected by the test_get_cohort_xxx() functions
def create_cohort_for_test_get_cohort_xxx(client):
    # Create a cohort to test against
    filters = {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    filterSet = {
        "idc_data_version": "1.0",
        "filters": filters
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.status_code == 200
    cohortResponse = response.json['cohort_properties']
    id = cohortResponse['cohort_id']
    return (id, filterSet)

# Create a big cohort with filter as expected by the test_get_cohort_xxx() functions
def create_big_cohort_for_test_get_cohort_xxx(client):
    # Create a cohort to test against
    filters = {
        "collection_id": ["tcga_luad"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    filterSet = {
        "idc_data_version": "1.0",
        "filters": filters
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.status_code == 200
    cohortResponse = response.json['cohort_properties']
    id = cohortResponse['cohort_id']
    return (id, filterSet)

# Utility to delete an existing cohort
def delete_cohort(client, id):
    response = client.delete("{}/{}/".format('v1/cohorts',id))
    assert response.content_type == 'application/json'
    assert response.status_code == 200


