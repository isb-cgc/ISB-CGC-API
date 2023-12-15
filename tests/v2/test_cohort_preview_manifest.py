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

# from settings import API_URL
from testing_config import API_URL, get_data, test_dev_api, auth_header
import json
import datetime
from testing_utils import _testMode
from google.cloud import bigquery


@_testMode
def test_invalid_keys(client, app):
    filters = {
        "age_at_diagnosis_btw": [65, 75],
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"]
    }

    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
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

    manifestPreviewBody = {
        "Cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                           data=json.dumps(manifestPreviewBody),
                           headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == "'cohort_def' is required in the body"

    manifestPreviewBody = {
        # "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                           data=json.dumps(manifestPreviewBody),
                           headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == "'cohort_def' is required in the body"

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "Fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                           data=json.dumps(manifestPreviewBody),
                           headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == 'Fields is an invalid body key'

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "Counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                           data=json.dumps(manifestPreviewBody),
                           headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == 'Counts is an invalid body key'

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "Group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                           data=json.dumps(manifestPreviewBody),
                           headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == 'Group_size is an invalid body key'

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": False,
        "SQL": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == 'SQL is an invalid body key'

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'Page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                           data=json.dumps(manifestPreviewBody),
                           headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == 'Page_size is an invalid body key'

    manifestPreviewBody = {
        # "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == "\'cohort_def\' is required in the body"

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        # "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == "fields is required in the body"

    cohort_def = {"name": "testcohort",
                  "Description": "Test description",
                  "filters": filters
                  }


    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == "'Description' is an invalid cohort_def key"

    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "Filters": filters
                  }

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000,
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert get_data(response)['message'] == "'Filters' is an invalid cohort_def key"

    return

@_testMode
def test_basic(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
        "age_at_diagnosis_btw": [65, 75],
        "collection_id": ["TCGA-RE%"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"]
    }

    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    fields = [
        'collection_id',
        'crdc_study_uuid',
        'crdc_series_uuid',
        'crdc_instance_uuid',
        'gcs_bucket',
        'gcs_url',
        'aws_bucket',
        'aws_url'
    ]

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": False,
        "sql": True,
        'page_size': 2000
    }

    # Get a manifest of the cohort's instances`
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
            data = json.dumps(manifestPreviewBody),
            headers=headers
        )
    assert response.status_code == 200

    cohort_def = get_data(response)['cohort_def']
    manifest = get_data(response)['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestPreviewBody["page_size"]}')]

    assert manifest['rowsReturned'] == len(bq_data)

    next_page = get_data(response)['next_page']
    assert next_page == ""

    rows = manifest['manifest_data']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))


@_testMode
def test_special_fields(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"],
        "age_at_diagnosis_btw": [65,75]
    }
    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis',
        'seriesinstanceuid',
        'studyDescription',
        'studyDate'
        ]

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": False,
        "group_size": False,
        "sql": True,
        'page_size': 2000
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = get_data(response)['cohort_def']
    manifest = get_data(response)['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestPreviewBody["page_size"]}')]

    assert manifest['rowsReturned'] == len(bq_data)

    next_page = get_data(response)['next_page']
    assert next_page == ""

    rows = manifest['manifest_data']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    for key in bq_data[0]:
        print(key)
        assert (set(row[key].isoformat() if isinstance(row[key], datetime.date) else row[key] for row in bq_data) == set(row[key] for row in rows))


@_testMode
def test_series_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    # app = Flask(__name__)
    # client = app.test_client()

    filters = {
        "age_at_diagnosis_btw": [65, 75],
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"]
    }
    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis',
        'seriesinstanceuid',
        ]

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = get_data(response)['cohort_def']
    manifest = get_data(response)['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestPreviewBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = get_data(response)['next_page']
    assert next_page == ""

    rows = manifest['manifest_data']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    assert 'group_size' in bq_data[0]
    assert 'instance_count' in bq_data[0]
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))
    # assert {'GCS_URL': 'gs://public-datasets-idc/0190fe71-7144-40ae-a24c-c8d21a99317d/01210a30-8395-498c-905f-6667db67101a.dcm'} in rows


@_testMode
def test_study_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
        "age_at_diagnosis_btw": [65, 75],
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"]
    }
    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis',
        'studyinstanceuid',
        ]

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = get_data(response)['cohort_def']
    manifest = get_data(response)['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestPreviewBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = get_data(response)['next_page']
    assert next_page == ""

    rows = manifest['manifest_data']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    assert 'group_size' in bq_data[0]
    assert 'instance_count' in bq_data[0]
    assert 'series_count' in bq_data[0]
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))


@_testMode
def test_patient_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
        "age_at_diagnosis_btw": [65, 75],
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"]
    }
    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis',
        'patientID',
        ]

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = get_data(response)['cohort_def']
    manifest = get_data(response)['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestPreviewBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = get_data(response)['next_page']
    assert next_page == ""

    rows = manifest['manifest_data']
    assert len(rows) == len(bq_data)
    assert manifest['totalFound'] == len(bq_data)
    assert 'group_size' in bq_data[0]
    assert 'instance_count' in bq_data[0]
    assert 'series_count' in bq_data[0]
    assert 'study_count' in bq_data[0]
    for key in bq_data[0]:
        print(key)
        assert (set(row[key] for row in bq_data) == set(row[key] for row in rows))


@_testMode
def test_collection_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
        "age_at_diagnosis_btw": [65, 75],
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"]
    }
    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    fields = [
        'collection_id',
        'modality',
        'race',
        'age_at_diagnosis'
        ]

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # query = gen_query(manifestPreviewBody)
    # bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = get_data(response)['cohort_def']
    manifest = get_data(response)['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestPreviewBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = get_data(response)['next_page']
    assert next_page == ""

    rows = manifest['manifest_data']
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


@_testMode
def test_version_granularity(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
        "age_at_diagnosis_btw": [65, 75],
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"]
    }
    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    fields = [
        'modality',
        'race',
        'age_at_diagnosis'
        ]

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 2000
    }

    # query = gen_query(manifestPreviewBody)
    # bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)

    # assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = get_data(response)['cohort_def']
    manifest = get_data(response)['manifest']
    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'] + f'LIMIT {manifestPreviewBody["page_size"]}')]


    assert manifest['rowsReturned'] == len(bq_data)

    next_page = get_data(response)['next_page']
    assert next_page == ""

    rows = manifest['manifest_data']
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


@_testMode
def test_paged(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
    filters = {
        "collection_id": ["TCGA-READ"],
        "Modality": ["ct", "mR"],
        "RACE": ["WHITE"],
        "age_at_diagnosis_btw": [1,100]
    }

    cohort_def = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

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

    manifestPreviewBody = {
        "cohort_def": cohort_def,
        "fields": fields,
        "counts": True,
        "group_size": True,
        "sql": True,
        'page_size': 500
    }

    response = client.post(f'{API_URL}/cohorts/manifest/preview',
                            data = json.dumps(manifestPreviewBody),
                            headers=headers)


    # assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort_def = get_data(response)['cohort_def']
    manifest = get_data(response)['manifest']

    next_page = get_data(response)['next_page']

    rows = manifest['manifest_data']
    assert len(rows) == 500
    # assert manifest['totalFound'] == len(bq_data)
    assert manifest['rowsReturned'] ==500

    assert next_page

    #Now get the remaining pages
    complete_manifest = manifest['manifest_data']
    totalRowsReturned = manifest['rowsReturned']

    while next_page:
        query_string = {
            'Next_Page': next_page,
            'PAGE_SIZE': 500
        }

        if test_dev_api:
            response = client.get(f'{API_URL}/cohorts/manifest/preview/nextPage',
                                params=query_string,
                                headers = headers)
        else:
            response = client.get(f'{API_URL}/cohorts/manifest/preview/nextPage',
                                query_string=query_string,
                                headers = headers)
        assert response.status_code == 200
        manifest = get_data(response)['manifest']
        next_page = get_data(response)['next_page']

        totalRowsReturned += manifest["rowsReturned"]
        complete_manifest.extend(manifest['manifest_data'])

    bq_data = [dict(row) for row in bq_client.query(cohort_def['sql'])]

    assert len(complete_manifest) == len(bq_data)
    for bq_key in bq_data[0]:
        api_key = next(api_key for api_key in rows[0].keys() if bq_key.lower()==api_key.lower())
        assert (set(row[bq_key] for row in bq_data) == set(row[api_key] for row in rows))
