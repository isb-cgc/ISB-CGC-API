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

from .cohort_utils import pretty_print_cohortObjects, merge, create_cohort, create_cohort_for_test_get_cohort_xxx, \
    create_big_cohort_for_test_get_cohort_xxx, delete_cohort


def test_doi(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'access_method': 'doi',
        'page_size': 2000
    }

    # Get a doi manifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert cohort['cohort_id']==id

    assert manifest['rowsReturned'] == 1638

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 1638
    assert manifest['totalFound'] == 1638
    assert 'dg.4DFC/0013f110-0928-4d66-ba61-7c3e80b48a68' in [row['doi'] for row in json_manifest]

    delete_cohort(client, id)


def test_url(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'access_method': 'url',
        'page_size': 2000
    }

    # Get a doi manifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert cohort['cohort_id']==id

    assert manifest['rowsReturned'] == 1638

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 1638
    assert manifest['totalFound'] == 1638
    assert 'gs://idc-tcia-tcga-read/dicom/1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508/1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631/1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597.dcm#1592638257658431' \
           in [row['url'] for row in json_manifest]

    delete_cohort(client, id)


def test_all(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = dict(
        sql = True,
        Collection_IDs = True,
        Patient_IDs = True,
        StudyInstanceUIDs = True,
        SeriesInstanceUIDs = True,
        SOPInstanceUIDs = True,
        Collection_DOIs = True,
        access_method =  'url',
        page_size = 2000
    )
    # Get a doi manifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert cohort['cohort_id']==id

    assert manifest['rowsReturned'] == 1638

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 1638
    assert manifest['totalFound'] == 1638
    assert 'TCGA-CL-5917' in [row['PatientID'] for row in json_manifest]
    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597' in [row['SOPInstanceUID'] for row in json_manifest]
    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631' in [row['SeriesInstanceUID'] for row in json_manifest]
    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508' in [row['StudyInstanceUID'] for row in json_manifest]
    assert 'tcga_read' in [row['collection_id'] for row in json_manifest]
    assert '10.7937/K9/TCIA.2016.F7PPNPNU' in [row['source_DOI'] for row in json_manifest]
    assert 'gs://idc-tcia-tcga-read/dicom/1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508/1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631/1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597.dcm#1592638257658431' \
           in [row['url'] for row in json_manifest]

    delete_cohort(client, id)


def test_paged_doi(client, app):

    (id, filterSet) = create_big_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'access_method': 'doi',
        'page_size': 5000
    }

    # Get a manifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']
    next_page = response.json['next_page']

    assert cohort['cohort_id']==id

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 5000
    assert manifest['totalFound'] == 21940
    assert manifest['rowsReturned'] ==5000

    assert next_page

    #Now get the remaining pages
    complete_manifest = manifest['json_manifest']
    totalRowsReturned = manifest['rowsReturned']

    while next_page:
        query_string = {
            'access_method': 'doi',
            'next_page': next_page,
            'page_size': 5000
        }

        # Get the list of objects in the cohort
        response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                    query_string = query_string)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        cohort = response.json['cohort']
        manifest = response.json['manifest']
        next_page = response.json['next_page']

        totalRowsReturned += manifest["rowsReturned"]
        complete_manifest.extend(manifest['json_manifest'])

    assert 'dg.4DFC/0009e98e-bca2-4a68-ada1-62e0a8b2dbaf' in \
           [row['doi'] for row in complete_manifest]
    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(complete_manifest)

    delete_cohort(client, id)


def test_paged_url(client, app):
    (id, filterSet) = create_big_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'access_method': 'url',
        'page_size': 5000
    }

    # Get a manifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                          query_string=query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']
    next_page = response.json['next_page']

    assert cohort['cohort_id'] == id

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 5000
    assert manifest['totalFound'] == 21940
    assert manifest['rowsReturned'] == 5000

    assert next_page

    # Now get the remaining pages
    complete_manifest = manifest['json_manifest']
    totalRowsReturned = manifest['rowsReturned']

    while next_page:
        query_string = {
            'access_method': 'url',
            'next_page': next_page,
            'page_size': 5000
        }

        # Get the list of objects in the cohort
        response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                              query_string=query_string)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        cohort = response.json['cohort']
        manifest = response.json['manifest']
        next_page = response.json['next_page']

        totalRowsReturned += manifest["rowsReturned"]
        complete_manifest.extend(manifest['json_manifest'])

    assert 'gs://idc-tcia-tcga-luad/dicom/1.3.6.1.4.1.14519.5.2.1.3983.9002.107656215131152599944682699489/1.3.6.1.4.1.14519.5.2.1.3983.9002.169653067901690682811265889199/1.3.6.1.4.1.14519.5.2.1.3983.9002.139964879860094005134659511427.dcm#1592637570041744' in \
           [row['url'] for row in complete_manifest]
    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(complete_manifest)

    delete_cohort(client, id)



