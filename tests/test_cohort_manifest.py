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

from settings import API_VERSION
from tests.testing_utils import create_cohort_for_test_get_cohort_xxx, \
    create_big_cohort_for_test_get_cohort_xxx, delete_cohort, find_v1_cohort_for_test_get_cohort_xxx, \
    find_v1_big_cohort_for_test_get_cohort_xxx, gen_query
from google.cloud import bigquery


## create_prior_version_cohorts.py can't create V1 cohorts
# def test_guid_v1(client, app):
#     filterSet = {
#         "filters": {
#             "BodyPartExamined": [
#                 "BLADDER",
#                 "BRAIN"
#             ]
#         },
#         "idc_data_version": "1.0"
#     }
#
#     (id, filterSet) = find_v1_cohort_for_test_get_cohort_xxx(client, filterSet)
#     assert id != -1
#
#     query_string = {
#         'CRDC_Instance_GUID': True,
#         'page_size': 2000
#     }
#
#     # Get a doi manifest of the cohort's instances
#     response = client.get("{}/manifest/{}".format('v1/cohorts', id),
#                 query_string = query_string)
#     assert response.content_type == 'application/json'
#     assert response.status_code == 200
#     cohort = response.json['cohort']
#     manifest = response.json['manifest']
#
#     assert cohort['cohort_id']==id
#
#     assert manifest['rowsReturned'] == 2000
#     assert manifest['totalFound'] == 802018
#
#     next_page = response.json['next_page']
#     assert next_page != ""
#
#     json_manifest = manifest['json_manifest']
#     assert len(json_manifest) == 2000
#     assert 'dg.4DFC/0000053b-bcd8-4697-9677-6710d7bbe0ec' in [row['CRDC_Instance_GUID'] for row in json_manifest]


def test_guid_active(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'sql': True,
        'crdc_study_uuid': "True",
        'crdc_series_uuid':True,
        'crdc_instance_uuid': True,
        # 'gcs_bucket': 'True',
        'gcs_url': False,
        # 'aws_bucket': False,
        'aws_url': 'False',
        'page_size': 2000,
    }

    query = gen_query(filterSet['filters'], query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.get(f"{API_VERSION}/cohorts/manifest/{id}/",
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in json_manifest))

    delete_cohort(client, id)


def test_url_active(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'gcs_url': True,
        'aws_url': True,
        'page_size': 2000,
    }

    query = gen_query(filterSet['filters'], query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.get(f"{API_VERSION}/cohorts/manifest/{id}/",
                query_string = query_string)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in json_manifest))

    delete_cohort(client, id)


def test_all_active(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    query_string = dict(
        sql = True,
        Collection_ID = True,
        PatientID = True,
        StudyInstanceUID = True,
        SeriesInstanceUID = True,
        SOPInstanceUID = True,
        Source_DOI = True,
        CRDC_Series_UUID = True,
        CRDC_Instance_UUID = True,
        CRDC_Study_UUID = True,
        GCS_URL = True,
        AWS_URL = True,
        page_size = 2000
    )

    query = gen_query(filterSet['filters'], query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]
    # Get a guid manifest of the cohort's instances
    response = client.get(f"{API_VERSION}/cohorts/manifest/{id}/",
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']

    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    for bq_key in bq_data[0]:
        api_key = next(api_key for api_key in json_manifest[0].keys() if bq_key.lower()==api_key.lower())
        assert (set(row[bq_key] for row in bq_data) == set(row[api_key] for row in json_manifest))

    delete_cohort(client, id)


def test_all_paged(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    query_string = dict(
        sql=True,
        Collection_ID=True,
        PatientID="True",
        StudyInstanceUID=True,
        SeriesInstanceUID=True,
        SOPInstanceUID=True,
        Source_DOI=True,
        CRDC_Study_UUID=True,
        CRDC_Series_UUID=True,
        CRDC_Instance_UUID=True,
        GCS_URL=True,
        AWS_URL=True,
        page_size=500
    )

    query = gen_query(filterSet['filters'], query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]
    response = client.get(f"{API_VERSION}/cohorts/manifest/{id}/",
                query_string = query_string)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    manifest = response.json['manifest']
    next_page = response.json['next_page']

    json_manifest = manifest['json_manifest']
    assert len(json_manifest) == 500
    assert manifest['totalFound'] == len(bq_data)
    assert manifest['rowsReturned'] ==500

    assert next_page

    #Now get the remaining pages
    complete_manifest = manifest['json_manifest']
    totalRowsReturned = manifest['rowsReturned']

    while next_page:
        query_string = {
            'Next_Page': next_page,
            'PAGE_SIZE': 500
        }

        # response = client.get(f"{API_VERSION}/cohorts/manifest/{id}/",
        #                       query_string=query_string)
        response = client.get(f'{API_VERSION}/cohorts/manifest/nextPage',
                               query_string=query_string)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        manifest = response.json['manifest']
        next_page = response.json['next_page']

        totalRowsReturned += manifest["rowsReturned"]
        complete_manifest.extend(manifest['json_manifest'])

    assert len(complete_manifest) == len(bq_data)
    for bq_key in bq_data[0]:
        api_key = next(api_key for api_key in json_manifest[0].keys() if bq_key.lower()==api_key.lower())
        assert (set(row[bq_key] for row in bq_data) == set(row[api_key] for row in json_manifest))

    delete_cohort(client, id)