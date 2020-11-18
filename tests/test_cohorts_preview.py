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


def test_cohort_preview_patients_eq(client, app):
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"],
            "age_at_diagnosis": [73]}}

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
        'sql': True,
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
    assert response.json['cohortObjects']['rowsReturned'] == 1

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['patient_id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-BM-6198'].sort()

    # Test that a _lte attribute can take more than one value
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"],
            "age_at_diagnosis": [72, 73]}}

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
        'sql': True,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] == 'Filters were improperly formatted.'


def test_cohort_preview_patients_lte(client, app):
    filterSet = {
        "idc_data_version": "1.0",
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
    assert response.json['cohortObjects']['rowsReturned'] == 1

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['patient_id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917'].sort()

    # Test that a _lte attribute can take more than one value
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"],
            "age_at_diagnosis_lte": [72, 73]}}

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
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] == 'Filters were improperly formatted.'


def test_cohort_preview_patients_btw(client, app):
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"],
            "age_at_diagnosis_btw": [10,75]}}

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
        'sql': True,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

#------------------------------------------------------------------

    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"],
            "age_at_diagnosis_btw": [72,73]}}

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
        'sql': True,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                           query_string=query_string,
                           data=json.dumps(cohortSpec),
                           headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert response.json['cohortObjects']['rowsReturned'] == 1

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['patient_id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917'].sort()

#------------------------------------------------------------------

    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"],
            "age_at_diagnosis_btw": [73,74]}}

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
        'sql': True,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                           query_string=query_string,
                           data=json.dumps(cohortSpec),
                           headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert response.json['cohortObjects']['rowsReturned'] == 1

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['patient_id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917'].sort()

#--------------------------------------------------------------

    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"],
            "age_at_diagnosis_btw": [10]}}

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
        'sql': True,
    }

    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] =='Filters were improperly formatted.'


def test_cohort_preview_sql(client, app):
    filterSet = {
        "idc_data_version": "1.0",
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
        'sql': True,
        'return_level': 'Patient',
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
    assert response.json['cohortObjects']['rowsReturned'] == 2
    assert cohort['sql'] == \
"""
            #standardSQL
    
        SELECT dicom_pivot_wave1.collection_id,dicom_pivot_wave1.PatientID
        FROM `idc-dev.metadata.dicom_pivot_wave1` dicom_pivot_wave1 
        
        JOIN `isb-cgc.TCGA_bioclin_v0.clinical_v1` clinical_v1
        ON dicom_pivot_wave1.PatientID = clinical_v1.case_barcode
    
        WHERE (dicom_pivot_wave1.collection_id = 'tcga_read') AND (dicom_pivot_wave1.Modality IN ('CT','MR')) AND (clinical_v1.race = 'WHITE')
        GROUP BY dicom_pivot_wave1.collection_id, dicom_pivot_wave1.PatientID
        ORDER BY dicom_pivot_wave1.PatientID ASC
        
        
    """


def test_cohort_preview_none(client, app):
    filterSet = {
        "idc_data_version": "1.0",
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
    assert response.json['cohortObjects']['totalFound'] == 0
    assert response.json['cohortObjects']['rowsReturned'] == 0
    assert response.json['cohortObjects']['collections'] == []
    assert response.json['next_page'] == None



def test_cohort_preview_collections(client, app):
    filterSet = {
        "idc_data_version": "1.0",
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
    assert response.json['cohortObjects']['totalFound'] == 1
    assert response.json['cohortObjects']['rowsReturned'] == 1
    assert response.json['next_page'] == None

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']


def test_cohort_preview_patients(client, app):
    filterSet = {
        "idc_data_version": "1.0",
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
    assert response.json['cohortObjects']['totalFound'] == 2
    assert response.json['cohortObjects']['rowsReturned'] == 2
    assert response.json['next_page'] == None

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['patient_id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()


def test_cohort_preview_studies(client, app):
    filterSet = {
        "idc_data_version": "1.0",
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
    assert response.json['cohortObjects']['totalFound']==3
    assert response.json['cohortObjects']['rowsReturned']==3
    assert response.json['next_page'] == None

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
            for collection in collections] == ['TCGA-READ']

    assert [patient['patient_id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()

    assert [study['StudyInstanceUID'].upper()
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']].sort() == \
       ['1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.329305334176079996095294344892',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917'].sort()


def test_cohort_preview_series(client, app):
    filterSet = {
        "idc_data_version": "1.0",
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
    assert response.json['cohortObjects']['totalFound']==31
    assert response.json['cohortObjects']['rowsReturned']==31
    assert response.json['next_page'] == None

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['patient_id'].upper()
        for collection in collections
        for patient in collection['patients']].sort() == \
        ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()

    assert [study['StudyInstanceUID']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']].sort() == \
        ['1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.329305334176079996095294344892',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917'].sort()

    assert len([series['SeriesInstanceUID']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']]) == 31

    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.322958037973582149511135969272' in \
        [series['SeriesInstanceUID']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']]


def test_cohort_preview_instances(client, app):
    filterSet = {
        "idc_data_version": "1.0",
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
    assert response.json['cohortObjects']['totalFound']==1638
    assert response.json['cohortObjects']['rowsReturned']==1638
    collections = response.json['cohortObjects']['collections']
    assert response.json['next_page'] == None

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']

    assert [patient['patient_id'].upper()
       for collection in collections
       for patient in collection['patients']].sort() == \
       ['TCGA-CL-5917', 'TCGA-BM-6198'].sort()

    assert [study['StudyInstanceUID']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']].sort() == \
        ['1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.329305334176079996095294344892',
        '1.3.6.1.4.1.14519.5.2.1.8421.4018.304030957341830836628192929917'].sort()

    assert len([series['SeriesInstanceUID']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']]) == 31

    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.322958037973582149511135969272' in \
        [series['SeriesInstanceUID']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']]


    assert len([instance['SOPInstanceUID']
        for collection in collections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for instance in series['instances']]) == 1638


# Get the result in chunks
def test_cohort_preview_instances_paged(client, app):
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["tcga_luad"],
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
    # Get the first page
    query_string = {
        'return_level': 'Instance',
    }
    # Get the list of objects in the cohort
    response = client.post('v1/cohorts/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort= response.json['cohort']
    cohortObjects = response.json['cohortObjects']
    allCollections = cohortObjects["collections"]
    assert cohortObjects['totalFound']==21940
    assert cohortObjects['rowsReturned']==10000


    job_reference = response.json['job_reference']
    next_page = response.json['next_page']
    assert job_reference
    assert next_page


    #Now get the data in 500 row chunks

    totalCollections = allCollections
    totalRowsReturned = cohortObjects['rowsReturned']

    while next_page:
        query_string = {
            'return_level': 'Instance',
            'job_reference': job_reference,
            'next_page': next_page
        }

        # Get the list of objects in the cohort
        # response = client.get("{}/{}/".format('v1/cohorts', id),
        #             query_string = query_string)
        response = client.post('v1/cohorts/preview',
                               query_string=query_string,
                               data=json.dumps(cohortSpec),
                               headers=headers)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        cohort = response.json['cohort']

        cohortObjects = response.json['cohortObjects']
        rowsReturned = cohortObjects["rowsReturned"]
        totalRowsReturned += rowsReturned
        collections = cohortObjects["collections"]
        merge(collections, allCollections, 0)
        allCollections.extend(collections)
        job_reference = response.json['job_reference']
        next_page = response.json['next_page']

    assert totalRowsReturned == cohortObjects['totalFound']

    allPatients = set([patient['patient_id'].upper()
       for collection in allCollections
       for patient in collection['patients']])
    totalPatients = set([patient['patient_id'].upper()
       for collection in totalCollections
       for patient in collection['patients']])
    assert allPatients == totalPatients

    allStudies = set([study['StudyInstanceUID']
        for collection in allCollections
        for patient in collection['patients']
        for study in patient['studies']])
    totalStudies = set([study['StudyInstanceUID']
        for collection in totalCollections
        for patient in collection['patients']
        for study in patient['studies']])
    assert allStudies == totalStudies

    allSeries = set([series['SeriesInstanceUID']
        for collection in allCollections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']])
    totalSeries = set([series['SeriesInstanceUID']
        for collection in totalCollections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']])
    assert allSeries == totalSeries

    allInstances = set([instance['SOPInstanceUID']
        for collection in allCollections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for instance in series['instances']])
    totalInstances = set([instance['SOPInstanceUID']
        for collection in totalCollections
        for patient in collection['patients']
        for study in patient['studies']
        for series in study['series']
        for instance in series['instances']])
    assert allInstances == totalInstances


    # # Get the list of objects in the cohort
    # response = client.post('v1/cohorts/preview',
    #                         query_string = query_string,
    #                         data = json.dumps(cohortSpec),
    #                         headers=headers)
    # assert response.content_type == 'application/json'
    # assert response.status_code == 200
    # cohortall= response.json['cohort']
    # allCollections = cohortall["cohortObjects"]["collections"]
    #
    # #Now get the data in 500 row chunks
    #
    # totalSchema = []
    # totalCollections = []
    # totalRowsReturned = 0
    #
    # fetch_count = 500
    # while True:
    #
    #     query_string = {
    #         'return_level': 'Instance',
    #         'fetch_count': fetch_count,
    #         'offset': totalRowsReturned,
    #     }
    #
    #     # Get the list of objects in the cohort
    #     response = client.post('v1/cohorts/preview',
    #                            query_string=query_string,
    #                            data=json.dumps(cohortSpec),
    #                            headers=headers)
    #     assert response.content_type == 'application/json'
    #     assert response.status_code == 200
    #     cohort = response.json['cohort']
    #
    #     cohortObjects = response.json['cohortObjects']
    #     rowsReturned = cohortObjects["rowsReturned"]
    #     totalRowsReturned += rowsReturned
    #     collections = cohortObjects["collections"]
    #     merge(collections, totalCollections, 0)
    #     if rowsReturned < fetch_count:
    #         break
    #
    # allPatients = [patient['patient_id'].upper()
    #    for collection in allCollections
    #    for patient in collection['patients']].sort()
    # totalPatients = [patient['patient_id'].upper()
    #    for collection in totalCollections
    #    for patient in collection['patients']].sort()
    # assert allPatients == totalPatients
    #
    # allStudies = [study['StudyInstanceUID']
    #     for collection in allCollections
    #     for patient in collection['patients']
    #     for study in patient['studies']].sort()
    # totalStudies = [study['StudyInstanceUID']
    #     for collection in totalCollections
    #     for patient in collection['patients']
    #     for study in patient['studies']].sort()
    # assert allStudies == totalStudies
    #
    # allSeries = [series['SeriesInstanceUID']
    #     for collection in allCollections
    #     for patient in collection['patients']
    #     for study in patient['studies']
    #     for series in study['series']].sort()
    # totalSeries = [series['SeriesInstanceUID']
    #     for collection in totalCollections
    #     for patient in collection['patients']
    #     for study in patient['studies']
    #     for series in study['series']].sort()
    # assert allSeries == totalSeries
    #
    # allInstances = [instance['SOPInstanceUID']
    #     for collection in allCollections
    #     for patient in collection['patients']
    #     for study in patient['studies']
    #     for series in study['series']
    #     for instance in series['instances']].sort()
    # totalInstances = [instance['SOPInstanceUID']
    #     for collection in totalCollections
    #     for patient in collection['patients']
    #     for study in patient['studies']
    #     for series in study['series']
    #     for instance in series['instances']].sort()
    # assert allInstances == totalInstances

