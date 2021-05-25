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

from .cohort_utils import create_cohort_for_test_get_cohort_xxx, \
    create_big_cohort_for_test_get_cohort_xxx, delete_cohort, find_v1_cohort_for_test_get_cohort_xxx, \
    find_v1_big_cohort_for_test_get_cohort_xxx


# We can't create V1 cohorts so, find an existing V1 cohort that has the filters expected by this test
def test_guid_v1(client, app):
    filterSet = {
        "filters": {
            "BodyPartExamined": [
                "BLADDER",
                "BRAIN"
            ]
        },
        "idc_data_version": "1.0"
    }

    (id, filterSet) = find_v1_cohort_for_test_get_cohort_xxx(client, filterSet)
    assert id != -1

    query_string = {
        'CRDC_Instance_GUID': True,
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

    assert manifest['rowsReturned'] == 2000
    assert manifest['totalFound'] == 802018

    next_page = response.json['next_page']
    assert next_page != ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 2000
    assert 'dg.4DFC/0000053b-bcd8-4697-9677-6710d7bbe0ec' in [row['CRDC_Instance_GUID'] for row in json_manifest]


def test_guid_active(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'CRDC_Instance_GUID': True,
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
    assert 'dg.4DFC/0013f110-0928-4d66-ba61-7c3e80b48a68' in [row['CRDC_Instance_GUID'] for row in json_manifest]

    delete_cohort(client, id)


def test_url_v1(client, app):
    filterSet = {
        "filters": {
            "BodyPartExamined": [
                "BLADDER",
                "BRAIN"
            ]
        },
        "idc_data_version": "1.0"
    }

    (id, filterSet) = find_v1_cohort_for_test_get_cohort_xxx(client, filterSet)

    query_string = {
        'GCS_URL': True,
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

    assert manifest['rowsReturned'] == 2000
    assert manifest['totalFound'] == 802018

    next_page = response.json['next_page']
    assert next_page != ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 2000
    assert {'GCS_URL': 'gs://idc_dev/0000053b-bcd8-4697-9677-6710d7bbe0ec.dcm'} in json_manifest


def test_url_active(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'GCS_URL': True,
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
    assert {'GCS_URL': 'gs://idc_dev/0013f110-0928-4d66-ba61-7c3e80b48a68.dcm'} in json_manifest

    delete_cohort(client, id)


def test_all_v1(client, app):
    filterSet = {
        "filters": {
          "AnatomicRegionSequence": [
            "T-42300:SRT"
          ]
        },
        "idc_data_version": "1.0"
      }

    (id, filterSet) = find_v1_cohort_for_test_get_cohort_xxx(client, filterSet)

    query_string = dict(
        sql = True,
        Collection_ID = True,
        Patient_ID = True,
        StudyInstanceUID = True,
        SeriesInstanceUID = True,
        SOPInstanceUID = True,
        Source_DOI = True,
        CRDC_Study_GUID = True,
        CRDC_Series_GUID = True,
        CRDC_Instance_GUID = True,
        GCS_URL = True,
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

    assert manifest['rowsReturned'] == 60

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 60
    assert manifest['totalFound'] == 60
    assert 'QIN-HEADNECK-01-0140' in [row['Patient_ID'] for row in json_manifest]
    assert '1.2.276.0.7230010.3.1.4.8323329.20668.1440004843.285026' in [row['SOPInstanceUID'] for row in json_manifest]
    assert '1.2.276.0.7230010.3.1.3.8323329.20668.1440004843.285025' in [row['SeriesInstanceUID'] for row in json_manifest]
    assert '1.3.6.1.4.1.14519.5.2.1.2744.7002.642123555147672466718059464827' in [row['StudyInstanceUID'] for row in json_manifest]
    assert 'qin_headneck' in [row['Collection_ID'] for row in json_manifest]
    assert '10.7937/K9/TCIA.2015.K0F5CGLI' in [row['Source_DOI'] for row in json_manifest]
    assert next(row for row in json_manifest if row['GCS_URL'] == 'gs://idc_dev/0534ab60-7e5a-459a-9c80-b87d1590aedf.dcm')
    assert next(row for row in json_manifest if row['CRDC_Study_GUID'] == 'dg.4DFC/2a8ac373-9f08-420b-b497-939101d0124d')
    assert next(row for row in json_manifest if row['CRDC_Series_GUID'] == 'dg.4DFC/4a9a581a-465f-4503-9c47-f5691c8181d5')
    assert next(row for row in json_manifest if row['CRDC_Instance_GUID'] == 'dg.4DFC/0534ab60-7e5a-459a-9c80-b87d1590aedf')


def test_all_active(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = dict(
        sql = True,
        Collection_ID = True,
        Patient_ID = True,
        StudyInstanceUID = True,
        SeriesInstanceUID = True,
        SOPInstanceUID = True,
        Source_DOI = True,
        CRDC_Series_GUID = True,
        CRDC_Instance_GUID = True,
        CRDC_Study_GUID = True,
        GCS_URL = True,
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

    delete_cohort(client, id)


def test_paged_guid_v1(client, app):

    filterSet = {
        "filters": {
            "tcia_tumorLocation": [
                "Esophagus",
                "Chest-abdomen-pelvis, Leg, Tspine"
            ]
        },
        "idc_data_version": "1.0"
    }

    (id, filterSet) = find_v1_cohort_for_test_get_cohort_xxx(client, filterSet)

    query_string = {
        'CRDC_Instance_GUID': True,
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
    assert manifest['totalFound'] == 26246
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

    assert 'dg.4DFC/fffd47d2-cc01-4363-874b-9ca846e256e8' in \
           [row['CRDC_Instance_GUID'] for row in complete_manifest]
    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(complete_manifest)


def test_paged_guid_active(client, app):

    (id, filterSet) = create_big_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'CRDC_Instance_GUID': True,
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
            'access_method': 'guid',
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
           [row['CRDC_Instance_GUID'] for row in complete_manifest]
    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(complete_manifest)

    delete_cohort(client, id)


def test_paged_url_v1(client, app):
    filterSet = {
        "filters": {
            "tcia_tumorLocation": [
                "Esophagus",
                "Chest-abdomen-pelvis, Leg, Tspine"
            ]
        },
        "idc_data_version": "1.0"
    }

    (id, filterSet) = find_v1_cohort_for_test_get_cohort_xxx(client, filterSet)

    query_string = {
        'GCS_URL': True,
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
    assert manifest['totalFound'] == 26246
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

    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(complete_manifest)
    assert next(row for row in json_manifest if row['GCS_URL'] == 'gs://idc_dev/fffd47d2-cc01-4363-874b-9ca846e256e8.dcm')


def test_paged_url_active(client, app):
    (id, filterSet) = create_big_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'GCS_URL': True,
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

    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(complete_manifest)
    assert next(row for row in json_manifest if row['GCS_URL'] == 'gs://idc_dev/0009e98e-bca2-4a68-ada1-62e0a8b2dbaf.dcm')

    delete_cohort(client, id)




