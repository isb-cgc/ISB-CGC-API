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
import copy
from deepmerge import always_merger, merge_or_raise

from django.conf import settings
logger = logging.getLogger(settings.LOGGER_NAME)

def pretty_print_cohortObjects(cohortObjects, indent=4):
    print(json.dumps(cohortObjects, sort_keys=True, indent=indent))

levels = ["collections", "patients", "studies", "series", "instances"]

# Merge two sets of collection data.
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
    id = cohortResponse['id']
    return (id, filterSet)

# Utility to delete an existing cohort
def delete_cohort(client, id):
    response = client.delete("{}/{}/".format('v1/cohorts',id))
    assert response.content_type == 'application/json'
    assert response.status_code == 200


def test_create_cohort(client, app):
    # Create a filter set
    filterSet = {
        "bioclin_version": "r9",
        "imaging_version": "0",
        "attributes": {
            "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
            "Modality": ["CT", "MR"],
            "Race": ["WHITE"]}}

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filterSet":filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    # cohortResponse = json.loads(response.json['cohortSpec'])
    cohortResponse = response.json

    assert cohortResponse['name']=="testcohort"
    assert cohortResponse['description']=="Test description"
    assert cohortResponse["filterSet"]["bioclin_version"]=="r9"
    assert "Modality" in cohortResponse["filterSet"]["attributes"]
    assert "TCGA-LUAD" in cohortResponse["filterSet"]["attributes"]["collection_id"]

    # Delete the cohort we just created
    delete_cohort(client, cohortResponse['id'])


def test_get_cohort_patients(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Patient',
        'fetch_count': 5000
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['id']==id
    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['totalRowsInCohort'] == 1638

    collections = cohort['cohortObjects']['collections']

    assert [collection['id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()

    delete_cohort(client, id)

def test_get_cohort_studies(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Study',
        'fetch_count': 5000

    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['id']==id
    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['totalRowsInCohort']==1638

    collections = cohort['cohortObjects']['collections']

    assert [collection['id'].upper()
            for collection in collections] == ['TCGA-READ']

    assert [patient['id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()

    assert [study['id'].upper()
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']].sort() == \
       ['1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.329305334176079996095294344892',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917'].sort()

    assert [accessMethod['access_url']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for accessMethod in study['AccessMethods']].sort() == \
       ['gs://gcs-public-data--healthcare-tcia-tcga-read/dicom/1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508',
        'gs://gcs-public-data--healthcare-tcia-tcga-read/dicom/1.3.6.1.4.1.14519.5.2.1.8421.4018.329305334176079996095294344892',
        'gs://gcs-public-data--healthcare-tcia-tcga-read/dicom/1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917'].sort()

    delete_cohort(client, id)

def test_get_cohort_series(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Series',
        'fetch_count': 5000
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['id']==id
    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['totalRowsInCohort']==1638

    collections = cohort['cohortObjects']['collections']

    assert [collection['id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
        ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()

    assert [study['id']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']].sort() == \
        ['1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.329305334176079996095294344892',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917'].sort()

    assert len([series['id']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']]) == 31

    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.322958037973582149511135969272' in \
        [series['id']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']]

    assert 'gs://gcs-public-data--healthcare-tcia-tcga-read/dicom/' \
       '1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917/' \
       '1.3.6.1.4.1.14519.5.2.1.8421.4018.234350234633941492462148996523' in \
        [accessMethod['access_url']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for accessMethod in series['AccessMethods']]
    # pretty_print_collections(collections)
    delete_cohort(client, id)


def test_get_cohort_instances(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Instance',
        'fetch_count': 5000
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['id']==id
    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['totalRowsInCohort']==1638
    collections = cohort['cohortObjects']['collections']

    assert [collection['id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['id'].upper()
       for collection in collections
       for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()

    assert [study['id']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']].sort() == \
        ['1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.329305334176079996095294344892',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917'].sort()

    assert len([series['id']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']]) == 31

    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.322958037973582149511135969272' in \
        [series['id']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']]

    assert 'gs://gcs-public-data--healthcare-tcia-tcga-read/dicom/' \
       '1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917/' \
       '1.3.6.1.4.1.14519.5.2.1.8421.4018.234350234633941492462148996523' in \
        [accessMethod['access_url']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for accessMethod in series['AccessMethods']]

    assert len([instance['id']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for instance in series['instances']]) == 1638

    assert 'gs://gcs-public-data--healthcare-tcia-tcga-read/dicom/' \
       '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508/' \
       '1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631/' \
       '1.3.6.1.4.1.14519.5.2.1.3671.4018.350542910477885137694058742820.dcm' in \
        [accessMethod['access_url']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for instance in series['instances']
        for accessMethod in instance['AccessMethods']]

    delete_cohort(client, id)


# Get the result in chunks
def test_get_cohort_instances_paged(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    # First get all the rows in one call
    query_string = {
        'return_level': 'Instance',
        'fetch_count': 5000,
        'offset': 0,
        'return_DOIs': False,
        'return_URLs': False,
        'return_filter': False,
    }
    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohortall= response.json['cohort']
    allCollections = cohortall["cohortObjects"]["collections"]

    #Now get the data in 500 row chunks

    totalSchema = []
    totalCollections = []
    totalRowsReturned = 0

    fetch_count = 500
    while True:

        query_string = {
            'return_level': 'Instance',
            'fetch_count': fetch_count,
            'offset': totalRowsReturned,
            'return_DOIs': False,
            'return_URLs': False,
            'return_filter': False,
        }

        # Get the list of objects in the cohort
        response = client.get("{}/{}/".format('v1/cohorts', id),
                    query_string = query_string)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        cohort = response.json['cohort']

        cohortObjects = cohort['cohortObjects']
        rowsReturned = cohortObjects["totalRowsInCohort"]
        totalRowsReturned += rowsReturned
        collections = cohortObjects["collections"]
        merge(collections, totalCollections, 0)
        if rowsReturned < fetch_count:
            break

    allPatients = [patient['id'].upper()
       for collection in allCollections
       for patient in collection['patients']].sort()
    totalPatients = [patient['id'].upper()
       for collection in totalCollections
       for patient in collection['patients']].sort()
    assert allPatients == totalPatients

    allStudies = [study['id']
        for collection in allCollections
        for patient in collection['patients']
        for study in patient['studies']].sort()
    totalStudies = [study['id']
        for collection in totalCollections
        for patient in collection['patients']
        for study in patient['studies']].sort()
    assert allStudies == totalStudies

    allSeries = [series['id']
        for collection in allCollections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']].sort()
    totalSeries = [series['id']
        for collection in totalCollections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']].sort()
    assert allSeries == totalSeries

    allInstances = [instance['id']
        for collection in allCollections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for instance in series['instances']].sort()
    totalInstances = [instance['id']
        for collection in totalCollections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for instance in series['instances']].sort()
    assert allInstances == totalInstances

    delete_cohort(client, id)

def test_list_cohorts(client,app):
    cohort1 = create_cohort(client)['id']
    cohort2 = create_cohort(client)['id']

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200

    cohorts = response.json['cohorts']
    assert len([cohort for cohort in cohorts if cohort['id']==int(cohort1)]) == 1
    assert len([cohort for cohort in cohorts if cohort['id']==int(cohort2)]) == 1

    delete_cohort(client, cohort1)
    delete_cohort(client, cohort2)


def test_delete_a_cohort(client, app):
    # Try deleting a
    # cohort that probably will never exist
    big_id = 2**64
    response = client.delete("{}/{}/".format('v1/cohorts', big_id))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == big_id
    assert cohorts[0]['result'] == "A cohort with the ID {} was not found!".format(str(big_id))

    # Create a cohort
    cohort1 = create_cohort(client)['id']
    # Delete the cohort we just created
    response = client.delete("{}/{}/".format('v1/cohorts', cohort1))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert cohorts[0]['result'] == "Cohort ID {} has been deleted.".format(str(cohort1))

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len([cohort for cohort in cohorts if cohort['id']==int(cohort1)]) == 0

    # Try deleting the cohort we just deleted
    response = client.delete("{}/{}/".format('v1/cohorts', cohort1))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert cohorts[0]['result'] == "Cohort ID {} was previously deleted.".format(str(cohort1))

def test_delete_cohorts(client, app):
    # Create a cohort
    cohort1 = create_cohort(client)['id']
    cohort2 = create_cohort(client)['id']

    # Delete the cohorts that we just created
    cohortIDs = [cohort1, cohort2]
    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.delete('/v1/cohorts', data=json.dumps(cohortIDs), headers=headers)
    assert response.status_code == 200
    cohorts = response.json['cohorts']

    assert len(cohorts) == 2
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert cohorts[0]['result'] == "Cohort ID {} has been deleted.".format(str(cohort1))
    assert cohorts[1]['cohort_id'] == int(cohort2)
    assert cohorts[1]['result'] == "Cohort ID {} has been deleted.".format(str(cohort2))

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200

    cohorts = response.json['cohorts']
    assert len([cohort for cohort in cohorts
                if cohort['id']==int(cohort1) or cohort['id']==int(cohort2)]) == 0

def test_delete_all_cohorts(client,app):
    # Create a couple of cohortsw
    create_cohort(client)
    create_cohort(client)

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']

    cohortIDs = [cohort['id'] for cohort in cohorts]
    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.delete('/v1/cohorts', data=json.dumps(cohortIDs), headers=headers)
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    for cohort in cohorts:
        assert cohort['result'] == "Cohort ID {} has been deleted.".format(str(cohort['cohort_id']))

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 0


# def test_cohort_preview(client, app):
#     # Create a filter set
#     collections = [{"program_name":"TCGA","collection_name":"BLCA","versions":["1.0"]}]
#     filter = {"program_name":["TCGA"], "project_short_name":["TCGA-LUAD","TCGA-KIRC"],"Modality":["CT","MR"]}
#     filterSet={"collections":collections,"filter":filter}
#
#     mimetype = ' application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }
#     response = client.post('/v1/cohorts/preview',data=json.dumps(filterSet), headers=headers)
#     assert response.content_type == mimetype
#
#     assert response.status_code == 200
#     data = json.loads(response.json['programs'])
#     assert len(list(filter(lambda program: program['short_name'] == "TCGA", data))) == 1
#     assert len(list(filter(lambda program: program['name'] == "The Cancer Genome Atlas", data))) == 1
