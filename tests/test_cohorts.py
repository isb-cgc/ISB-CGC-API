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


from .cohort_utils import pretty_print_cohortObjects, merge, create_cohort, create_cohort_for_test_get_cohort_xxx, create_big_cohort_for_test_get_cohort_xxx, delete_cohort


# Test filter schema validation
def test_create_cohort_schema_validation(client, app):
    # Create an invalid filter set
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
            # Undefined attribute
            "Modalityx": ["CT", "MR"],
            "race": ["WHITE"]}}

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filterSet":filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    cohortResponse = response.json
    assert cohortResponse['message']=='Cohort information was improperly formatted - cohort not created.'

    # Create an invalid filter set
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"]}}

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filterSet":filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    data = json.dumps(cohortSpec)
    # Corrupt the formatting
    data = data.replace('["CT"', '"CT"')

    response = client.post('/v1/cohorts', data=data, headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 400
    cohortResponse = response.json
    assert cohortResponse['message']=='The JSON provided in this request appears to be improperly formatted.'


# Merge two sets of collection data.
def test_create_cohort(client, app):
    # Create a filter set
    filterSet = {
        "idc_data_version": "1.0",
        "filters": {
            "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"]}}

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filterSet":filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohortResponse = response.json['cohort_properties']

    assert cohortResponse['name']=="testcohort"
    assert cohortResponse['description']=="Test description"
    # assert len(cohortResponse['filterSet']) == 1
    assert cohortResponse["filterSet"]["idc_data_version"]=="1.0"
    assert 'race' in cohortResponse['filterSet']['filters'] and \
           cohortResponse['filterSet']['filters']['race'] == ['WHITE']
    assert 'Modality' in cohortResponse['filterSet']['filters'] and \
           cohortResponse['filterSet']['filters']['Modality'] == ['CT', 'MR']
    assert 'collection_id' in cohortResponse['filterSet']['filters'] and \
           cohortResponse['filterSet']['filters']['collection_id'] == ['TCGA-LUAD', 'TCGA-KIRC']

    # Delete the cohort we just created
    delete_cohort(client, cohortResponse['cohort_id'])

def test_get_cohort_sql(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Collection',
        'sql': True,
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['cohort_id']==id
    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet

    assert cohort['sql'] == \
"""
            #standardSQL
    
        SELECT dicom_pivot_wave1.collection_id
        FROM `idc-dev.metadata.dicom_pivot_wave1` dicom_pivot_wave1 
        
        JOIN `isb-cgc.TCGA_bioclin_v0.clinical_v1` clinical_v1
        ON dicom_pivot_wave1.PatientID = clinical_v1.case_barcode
    
        WHERE (dicom_pivot_wave1.Modality IN ('CT','MR')) AND (dicom_pivot_wave1.collection_id = 'tcga_read') AND (clinical_v1.race = 'WHITE')
        GROUP BY dicom_pivot_wave1.collection_id
        ORDER BY dicom_pivot_wave1.collection_id ASC
        
        
    """

    delete_cohort(client, id)

def test_get_cohort_none(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'None',
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['cohort_id']==id
    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert response.json['cohortObjects']['totalFound'] == 0
    assert response.json['cohortObjects']['rowsReturned'] == 0
    assert response.json['cohortObjects']['collections'] == []
    assert response.json['next_page'] == None

    delete_cohort(client, id)

def test_get_cohort_collections(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Collection',
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['cohort_id']==id
    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert response.json['cohortObjects']['totalFound'] == 1
    assert response.json['cohortObjects']['rowsReturned'] == 1
    assert response.json['next_page'] == None

    collections = response.json['cohortObjects']['collections']

    assert [collection['collection_id'].upper()
        for collection in collections] == ['TCGA-READ']

    delete_cohort(client, id)

def test_get_cohort_patients(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Patient',
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['cohort_id']==id
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

    delete_cohort(client, id)

def test_get_cohort_studies(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Study',
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['cohort_id']==id
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

    delete_cohort(client, id)

def test_get_cohort_series(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Series',
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['cohort_id']==id
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

    delete_cohort(client, id)


def test_get_cohort_instances(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'return_level': 'Instance',
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']

    assert cohort['cohort_id']==id
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

    delete_cohort(client, id)


# Get the result in chunks
def test_get_cohort_instances_paged(client, app):

    (id, filterSet) = create_big_cohort_for_test_get_cohort_xxx(client)

    # Get the first page
    query_string = {
        'return_level': 'Instance',
        'page_size': 5000
    }

    # Get the first page of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort= response.json['cohort']
    cohortObjects = response.json['cohortObjects']
    allCollections = cohortObjects["collections"]
    assert cohortObjects['totalFound']==21940
    assert cohortObjects['rowsReturned']==5000

    job_reference = response.json['job_reference']
    next_page = response.json['next_page']
    assert job_reference
    assert next_page


    #Now get the remaining pages
    totalCollections = allCollections
    totalRowsReturned = cohortObjects['rowsReturned']

    while next_page:
        query_string = {
            'return_level': 'Instance',
            'job_reference': job_reference,
            'next_page': next_page,
            'page_size': 5000
        }

        # Get the list of objects in the cohort
        response = client.get("{}/{}/".format('v1/cohorts', id),
                    query_string = query_string)
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

    delete_cohort(client, id)

def test_list_cohorts(client,app):
    cohort0 = create_cohort(client)['cohort_id']
    cohort1 = create_cohort(client)['cohort_id']

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
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
    response = client.delete("{}/{}/".format('v1/cohorts', big_id))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == big_id
    assert cohorts[0]['result']['message'] == "A cohort with the ID {} was not found!".format(str(big_id))

    # Create a cohort
    cohort1 = create_cohort(client)['cohort_id']
    # Delete the cohort we just created
    response = client.delete("{}/{}/".format('v1/cohorts', cohort1))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert re.sub(r'\(.*\) ',r'',cohorts[0]['result']['notes'])== \
           "Cohort {} has been deleted.".format(str(cohort1))

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len([cohort for cohort in cohorts if cohort['cohort_id']==int(cohort1)]) == 0

    # Try deleting the cohort we just deleted
    response = client.delete("{}/{}/".format('v1/cohorts', cohort1))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 1
    assert cohorts[0]['cohort_id'] == int(cohort1)
    assert cohorts[0]['result']['message'] == "Cohort ID {} has already been deleted.".format(str(cohort1))

def test_delete_cohorts(client, app):
    # Create a cohort
    cohort0 = create_cohort(client)['cohort_id']
    cohort1 = create_cohort(client)['cohort_id']

    # Delete the cohorts that we just created
    cohortIDs = {"cohorts": [cohort0, cohort1]}
    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.delete('/v1/cohorts', data=json.dumps(cohortIDs), headers=headers)
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
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200

    cohorts = response.json['cohorts']
    assert len([cohort for cohort in cohorts
                if cohort['cohort_id']==int(cohort0) or cohort['cohort_id']==int(cohort1)]) == 0

def test_delete_all_cohorts(client,app):
    # Create a couple of cohortsw
    create_cohort(client)
    create_cohort(client)

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']

    cohortIDs = {"cohorts":[cohort['cohort_id'] for cohort in cohorts]}
    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.delete('/v1/cohorts', data=json.dumps(cohortIDs), headers=headers)
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    for cohort in cohorts:
        # assert cohort['result'] == "Cohort ID {} has been deleted.".format(str(cohort['cohort_id']))
        assert re.sub(r'\(.*\) ',r'',cohort['result']['notes'])== \
               "Cohort {} has been deleted.".format(str(cohort['cohort_id']))

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = response.json['cohorts']
    assert len(cohorts) == 0


