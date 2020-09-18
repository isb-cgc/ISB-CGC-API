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

from tests.cohort_utils import merge, pretty_print_cohortObjects, create_cohort_for_test_get_cohort_xxx, delete_cohort

def pretty_print_cohortObjects(cohortObjects, indent=4):
    print(json.dumps(cohortObjects, sort_keys=True, indent=indent))

levels = ["collections", "patients", "studies", "series", "instances"]


def test_cohort_preview_patients_lte(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"],
            "age_at_diagnosis_lte": [72]}}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    query_string = {
        'return_level': 'Patient',
        'fetch_count': 5000,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['rowsReturned'] == 1

    collections = cohort['cohortObjects']['collections']

    assert [collection['id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917'].sort()


def test_cohort_preview_manifest(client, app):

    filterSet = {
        "idc_version": "",
        "filters": {
            "collection_id": ["TCGA-READ"],
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

    query_string = {
        'access_class': 'url',
        'fetch_count': 5000,
    }

    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    manifest = response.json['manifest']
    assert manifest['accessMethods']['type'] == 'gs'
    assert manifest['accessMethods']['region'] == 'us'
    assert len(manifest['accessMethods']['urls']) == 1638
    assert len(manifest['accessMethods']['dois']) == 0
    assert 'gs://idc-tcia-tcga-read/dicom/1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508/1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631/1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597.dcm#1592638257658431' \
        in manifest['accessMethods']['urls']

    query_string = {
        'access_class': 'doi',
        'fetch_count': 5000,
    }

    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    manifest = response.json['manifest']
    assert manifest['accessMethods']['type'] == 'gs'
    assert manifest['accessMethods']['region'] == 'us'
    assert len(manifest['accessMethods']['urls']) == 0
    assert len(manifest['accessMethods']['dois']) == 0


def test_cohort_preview_sql(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
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
    query_string = {
        'return_sql': True,
        'return_level': 'Patient',
        'fetch_count': 5000,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['rowsReturned'] == 2
    assert cohort['cohortObjects']['sql'] == \
"""	(
            #standardSQL
    
        SELECT dicom_all.collection_id,dicom_all.PatientID
        FROM `idc-dev-etl.idc_tcia_views_mvp_wave0.dicom_all` dicom_all 
        
        JOIN `isb-cgc.TCGA_bioclin_v0.clinical_v1` clinical_v1
        ON dicom_all.PatientID = clinical_v1.case_barcode
    
        WHERE (dicom_all.collection_id = 'tcga_read') AND (dicom_all.Modality IN ('CT','MR')) AND (clinical_v1.race = 'WHITE')
        GROUP BY dicom_all.collection_id, dicom_all.PatientID
        ORDER BY dicom_all.PatientID ASC
        
        
    )
	UNION ALL
"""


def test_cohort_preview_none(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
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
    query_string = {
        'return_level': 'None',
        'fetch_count': 5000,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert not 'cohortObjects' in cohort


def test_cohort_preview_collectionss(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
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
    query_string = {
        'return_level': 'Collection',
        'fetch_count': 5000,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['rowsReturned'] == 1

    collections = cohort['cohortObjects']['collections']

    assert [collection['id'].upper()
        for collection in collections] == ['TCGA-READ']


def test_cohort_preview_patients(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
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
    query_string = {
        'return_level': 'Patient',
        'fetch_count': 5000,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['rowsReturned'] == 2

    collections = cohort['cohortObjects']['collections']

    assert [collection['id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()


def test_cohort_preview_studies(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
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
    query_string = {
        'return_level': 'Study',
        'fetch_count': 5000,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['rowsReturned']==3

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


def test_cohort_preview_series(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
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
    query_string = {
        'return_level': 'Series',
        'fetch_count': 5000,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['rowsReturned']==31

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


def test_cohort_preview_instances(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
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
    query_string = {
        'return_level': 'Instance',
        'fetch_count': 5000
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert cohort['cohortObjects']['rowsReturned']==1638
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


    assert len([instance['id']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for instance in series['instances']]) == 1638


# Get the result in chunks
def test_cohort_preview_instances_paged(client, app):
    filterSet = {
        "idc_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
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
    query_string = {
        'return_level': 'Instance',
        'fetch_count': 5000,
        'offset': 0,
        # 'return_DOIs': False,
        # 'return_URLs': False,
        # 'return_filter': False,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
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
        }

        # Get the list of objects in the cohort
        response = client.post('v1/cohorts/preview',
                               query_string=query_string,
                               data=json.dumps(cohortSpec),
                               headers=headers)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        cohort = response.json['cohort']

        cohortObjects = cohort['cohortObjects']
        rowsReturned = cohortObjects["rowsReturned"]
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

