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

def test_guid(client, app):

    filters = {
        "collection_id": ["TCGA-READ"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"],
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'sql': False,
        'CRDC_Instance_GUID': True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert manifest['rowsReturned'] == 1638

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 1638
    assert manifest['totalFound'] == 1638
    assert 'dg.4DFC/0013f110-0928-4d66-ba61-7c3e80b48a68' in [row['CRDC_Instance_GUID'] for row in json_manifest]


def test_url(client, app):

    filters = {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'GCS_URL': True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert manifest['rowsReturned'] == 1638

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 1638
    assert manifest['totalFound'] == 1638
    assert {'GCS_URL': 'gs://idc_dev/0013f110-0928-4d66-ba61-7c3e80b48a68.dcm'} in json_manifest


def test_SOPInstanceUID(client, app):

    filters = {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"],
        "SOPInstanceUID": ["1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597"]}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'GCS_URL': True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert manifest['rowsReturned'] == 1

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 1
    assert manifest['totalFound'] == 1
    assert {'GCS_URL': 'gs://idc_dev/de364433-4eaf-440e-b714-6c8b7cf3c613.dcm'} in json_manifest


def test_all(client, app):

    filters = {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = dict(
        sql=True,
        Collection_ID=True,
        Patient_ID=True,
        StudyInstanceUID=True,
        SeriesInstanceUID=True,
        SOPInstanceUID=True,
        Source_DOI=True,
        CRDC_Study_GUID=True,
        CRDC_Series_GUID=True,
        CRDC_Instance_GUID=True,
        GCS_URL=True,
        page_size=2000
    )
    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert manifest['rowsReturned'] == 1638

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 1638
    assert manifest['totalFound'] == 1638
    assert 'TCGA-CL-5917' in [row['Patient_ID'] for row in json_manifest]
    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597' in [row['SOPInstanceUID'] for row in json_manifest]
    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631' in [row['SeriesInstanceUID'] for row in json_manifest]
    assert '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508' in [row['StudyInstanceUID'] for row in json_manifest]
    assert 'tcga_read' in [row['Collection_ID'] for row in json_manifest]
    assert '10.7937/K9/TCIA.2016.F7PPNPNU' in [row['Source_DOI'] for row in json_manifest]
    assert next(row for row in json_manifest if row['GCS_URL'] == 'gs://idc_dev/0013f110-0928-4d66-ba61-7c3e80b48a68.dcm')
    assert next(row for row in json_manifest if row['CRDC_Study_GUID'] == 'dg.4DFC/7efeae5d-6263-4184-9ad4-8df22720ada9')
    assert next(row for row in json_manifest if row['CRDC_Series_GUID'] == 'dg.4DFC/67e22f90-36e1-40aa-88bb-9b2efb5616f2')
    assert next(row for row in json_manifest if row['CRDC_Instance_GUID'] == 'dg.4DFC/0013f110-0928-4d66-ba61-7c3e80b48a68')


def test_paged_doi(client, app):
    filters = {
        "collection_id": ["tcga_luad"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'CRDC_Instance_GUID': True,
        'page_size': 5000
    }

    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']
    next_page = response.json['next_page']

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
            'access_method': 'guid',
            'next_page': next_page,
            'page_size': 5000
        }

        response = client.post('v1/cohorts/preview/manifest',
                               query_string=query_string,
                               data=json.dumps(cohortSpec),
                               headers=headers)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        cohort = response.json['cohort']
        manifest = response.json['manifest']
        next_page = response.json['next_page']

        totalRowsReturned += manifest["rowsReturned"]
        complete_manifest.extend(manifest['json_manifest'])

    assert 'dg.4DFC/0009e98e-bca2-4a68-ada1-62e0a8b2dbaf' in \
           [row['CRDC_Instance_GUID'] for row in complete_manifest]
    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(complete_manifest)


def test_paged_url(client, app):

    filters = {
        "tcia_species": ["Human"],
        "collection_id": ["tcga_luad"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'GCS_URL': True,
        'page_size': 5000
    }

    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']
    next_page = response.json['next_page']

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

        response = client.post('v1/cohorts/preview/manifest',
                               query_string=query_string,
                               data=json.dumps(cohortSpec),
                               headers=headers)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        cohort = response.json['cohort']
        manifest = response.json['manifest']
        next_page = response.json['next_page']

        totalRowsReturned += manifest["rowsReturned"]
        complete_manifest.extend(manifest['json_manifest'])
    assert {'GCS_URL': 'gs://idc_dev/0009e98e-bca2-4a68-ada1-62e0a8b2dbaf.dcm'} in json_manifest
    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(complete_manifest)

# This test submits an empty filter which means that all instances are returned.
# Takes a lot of time and bandwidth. Uncomment to run
# def test_paged_guid_all_instances(client, app):
#
#     import time
#
#     cohortSpec = {
#         "name": "mycohort",
#         "description": "Example description",
#         "filters": {}
#         }
#     }
#     query_string = dict(
#         access_method='guid',
#         page_size=40000000
#     )
#
#     mimetype = ' application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }
#
#     start = time.time()
#
#     response = client.post('v1/cohorts/preview/manifest',
#                            query_string=query_string,
#                            data=json.dumps(cohortSpec),
#                            headers=headers)
#
#     elapsed = time.time()-start
#     totalTime = elapsed
#
#     # Check that there wasn't an error with the request
#     if response.status_code != 200:
#         # Print the error code and message if something went wrong
#         print(response.json())
#
#     # print(json.dumps(response.json(), sort_keys=True, indent=4))
#
#     totalRows = response.json['manifest']['rowsReturned']
#     totalBytes = len(json.dumps(response.json))
#     next_page = response.json['next_page']
#     print('totalRows: {}, totalBytes: {}, next_page: {}, time: {}, rate: {}'.format(
#         totalRows, totalBytes, next_page[:16], elapsed, len(json.dumps(response.json))/elapsed
#     ))
#
#     while next_page:
#         query_string['next_page'] = response.json['next_page']
#
#         start = time.time()
#         response = client.post('v1/cohorts/preview/manifest',
#                                query_string=query_string,
#                                data=json.dumps(cohortSpec),
#                                headers=headers)
#
#         elapsed = time.time() - start
#         totalTime += elapsed
#
#         # Check that there wasn't an error with the request
#         if response.status_code != 200:
#             # Print the error code and message if something went wrong
#             print(response.json)
#             break
#
#         totalRows += response.json['manifest']['rowsReturned']
#         totalBytes += len(json.dumps(response.json))
#         next_page = response.json['next_page']
#
#         print('totalRows: {}, totalBytes: {}, next_page: {}, time: {}, rate: {}'.format(
#             totalRows, totalBytes, next_page[:16], elapsed, len(json.dumps(response.json)) / elapsed
#         ))
#
#     print('Total time: {}, rate: {}'.format(totalTime, totalBytes/totalTime))
