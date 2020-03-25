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

import logging
import json

from django.conf import settings
logger = logging.getLogger(settings.LOGGER_NAME)


levels = ["collections", "patients", "studies", "series", "instances"]

def pretty_print_cohortObjects(cohortObjects, indent=4):
    print(json.dumps(cohortObjects, sort_keys=True, indent=indent))

def merge(src, dst, level):
  for src_item in src:
        found = False
        for dst_item in dst:
            if src_item["id"] == dst_item["id"]:
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
        "bioclin_version": "r9",
        "imaging_version": "0",
        "attributes": {
            "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
            "Modality": ["CT", "MR"],
            "Race": ["WHITE"]}}

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
#    cohortResponse = json.loads(response.json['cohortSpec'])
    cohortResponse = response.json

    return cohortResponse

# Create a cohort with filter as expected by the test_get_cohort_xxx() functions
def create_cohort_for_test_get_cohort_xxx(client):
    # Create a cohort to test against
    attributes = {
        "collection_id": ["TCGA-READ"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]}
    filterSet = {
        "bioclin_version": "r9",
        "imaging_version": "0",
        "attributes": attributes}

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
    cohortResponse = response.json
    id = cohortResponse['cohort_id']
    return (id, filterSet)

# Utility to delete an existing cohort
def delete_cohort(client, id):
    response = client.delete("{}/{}/".format('v1/cohorts',id))
    assert response.content_type == 'application/json'
    assert response.status_code == 200


