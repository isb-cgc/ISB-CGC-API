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
import datetime
from testing_config import VERSIONS, API_VERSION
from testing_utils import create_cohort_for_test_get_cohort_xxx, \
    delete_cohort, \
    gen_query
from google.cloud import bigquery

mimetype = ' application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def test_invalid_keys(client, app):
    id = 1

    fields = [
        'crdc_study_uuid',
        'crdc_series_uuid',
        'crdc_instance_uuid',
        'gcs_bucket',
        'gcs_url',
        'aws_bucket',
        'aws_url'
    ]

    manifestBody = {
        "Fields": fields,
        "counts": False,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f"{API_VERSION}/cohorts/manifest/{id}/",
                           data=json.dumps(manifestBody),
                           headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] == 'Fields is an invalid body key'

    manifestBody = {
        "fields": fields,
        "Counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f"{API_VERSION}/cohorts/manifest/{id}/",
                           data=json.dumps(manifestBody),
                           headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] == 'Counts is an invalid body key'

    manifestBody = {
        "fields": fields,
        "counts": True,
        "Group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f"{API_VERSION}/cohorts/manifest/{id}/",
                           data=json.dumps(manifestBody),
                           headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] == 'Group_size is an invalid body key'

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": False,
        "SQL": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f"{API_VERSION}/cohorts/manifest/{id}/",
                            data = json.dumps(manifestBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] == 'SQL is an invalid body key'

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'Page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f"{API_VERSION}/cohorts/manifest/{id}/",
                           data=json.dumps(manifestBody),
                           headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] == 'Page_size is an invalid body key'


    manifestBody = {
        # "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f"{API_VERSION}/cohorts/manifest/{id}/",
                            data = json.dumps(manifestBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert response.json['message'] == "fields is required in the body"

    return


def test_basic(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    fields = [
        'crdc_study_uuid',
        'crdc_series_uuid',
        'crdc_instance_uuid',
        'gcs_bucket',
        'gcs_url',
        'aws_bucket',
        'aws_url'
    ]

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }
    # query = gen_query(filterSet['filters'], query_string)
    # bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.post(f"{API_VERSION}/cohorts/manifest/{id}/",
                          data=json.dumps(manifestBody),
                          headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200

    cohort_def = response.json['cohort_def']
    manifest = response.json['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestBody["page_size"]}')]

    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    rows = manifest['rows']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))

    # json_manifest = manifest['json_manifest']
    # assert len(json_manifest) == len(bq_data)
    # assert manifest['totalFound'] == len(bq_data)
    # for key in bq_data[0]:
    #     print(key)
    #     assert (set(row[key] for row in bq_data) == set(row[key] for row in json_manifest))

    delete_cohort(client, id)


def test_special_fields(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)


    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis',
        'seriesinstanceuid',
        'studyDescription',
        'studyDate',
        "patientage",
        "patientsex",
        "patientsize",
        "patientweight"
        ]

    manifestBody = {
        "fields": fields,
        "counts": False,
        "group_size": False,
        "sql": True,
        'page_size': 2000
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/{id}',
                            data = json.dumps(manifestBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = response.json['cohort_def']
    manifest = response.json['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestBody["page_size"]}')]

    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    rows = manifest['rows']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    for key in bq_data[0]:
        print(key)
        assert (set(row[key].isoformat() if isinstance(row[key], datetime.date) else row[key] for row in bq_data) == set(row[key] for row in rows))

def test_series_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis',
        'seriesinstanceuid',
        ]

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/{id}',
                            data = json.dumps(manifestBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = response.json['cohort_def']
    manifest = response.json['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    rows = manifest['rows']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    assert 'group_size' in bq_data[0]
    assert 'instance_count' in bq_data[0]
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))
    # assert {'GCS_URL': 'gs://public-datasets-idc/0190fe71-7144-40ae-a24c-c8d21a99317d/01210a30-8395-498c-905f-6667db67101a.dcm'} in rows


def test_study_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis',
        'studyinstanceuid',
        ]

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/{id}',
                            data = json.dumps(manifestBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = response.json['cohort_def']
    manifest = response.json['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    rows = manifest['rows']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    assert 'group_size' in bq_data[0]
    assert 'instance_count' in bq_data[0]
    assert 'series_count' in bq_data[0]
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))


def test_patient_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)
    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis',
        'patientID',
        ]

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/{id}',
                            data = json.dumps(manifestBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = response.json['cohort_def']
    manifest = response.json['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    rows = manifest['rows']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    assert 'group_size' in bq_data[0]
    assert 'instance_count' in bq_data[0]
    assert 'series_count' in bq_data[0]
    assert 'study_count' in bq_data[0]
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))


def test_collection_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)
    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis'
        ]

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # query = gen_query(manifestBody)
    # bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/{id}',
                            data = json.dumps(manifestBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = response.json['cohort_def']
    manifest = response.json['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    rows = manifest['rows']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    assert 'group_size' in bq_data[0]
    assert 'instance_count' in bq_data[0]
    assert 'series_count' in bq_data[0]
    assert 'study_count' in bq_data[0]
    assert 'patient_count' in bq_data[0]
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))


def test_version_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    fields = [
        'modality',
        'race',
        'age_at_diagnosis'
        ]

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # query = gen_query(manifestBody)
    # bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/{id}',
                            data = json.dumps(manifestBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = response.json['cohort_def']
    manifest = response.json['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = response.json['next_page']
    assert next_page == ""

    rows = manifest['rows']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    assert 'group_size' in bq_data[0]
    assert 'instance_count' in bq_data[0]
    assert 'series_count' in bq_data[0]
    assert 'study_count' in bq_data[0]
    assert 'patient_count' in bq_data[0]
    assert 'collection_count' in bq_data[0]
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))


def test_paged(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    id, filterSet = create_cohort_for_test_get_cohort_xxx(client)

    fields = [
        'Collection_ID',
        'PatientID',
        'StudyInstanceUID',
        'SeriesInstanceUID',
        'SOPInstanceUID',
        'Source_DOI',
        'CRDC_Study_UUID',
        'CRDC_Series_UUID',
        'CRDC_Instance_UUID',
        'GCS_URL',
        'AWS_URL'
        ]

    manifestBody = {
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 500
    }

    response = client.post(f'{API_VERSION}/cohorts/manifest/{id}',
                            data = json.dumps(manifestBody),
                            headers=headers)


    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = response.json['cohort_def']
    manifest = response.json['manifest']

    next_page = response.json['next_page']

    rows = manifest['rows']
    assert len(rows) == 500
    # assert manifest['totalFound'] == len(bq_data)
    assert manifest['rowsReturned'] ==500

    assert next_page

    #Now get the remaining pages
    complete_manifest = manifest['rows']
    totalRowsReturned = manifest['rowsReturned']

    while next_page:
        query_string = {
            'Next_Page': next_page,
            'PAGE_SIZE': 500
        }

        response = client.get(f'{API_VERSION}/cohorts/manifest/nextPage',
                               query_string=query_string )
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        manifest = response.json['manifest']
        next_page = response.json['next_page']

        totalRowsReturned += manifest["rowsReturned"]
        complete_manifest.extend(manifest['rows'])

    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'])]

    assert len(complete_manifest) == len(bq_data)
    for bq_key in bq_data[0]:
        api_key = next(api_key for api_key in rows[0].keys() if bq_key.lower()==api_key.lower())
        assert (set(row[bq_key] for row in bq_data) == set(row[api_key] for row in rows))
