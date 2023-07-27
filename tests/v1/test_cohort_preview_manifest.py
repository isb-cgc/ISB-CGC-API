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

# from settings import API_VERSION
from testing_config import VERSIONS, API_VERSION

import json
from testing_utils import gen_query
from testing_config import VERSIONS
from google.cloud import bigquery


def test_invalid_filter(client, app):

        filters = {
            "collection_id": ["TCGA-READ"],
            "Modality": ["ct", "mR"],
            "RACE": ["WHITE"],
            "age_at_diagnosis_btw": [1, 100],
            "foo": ["bar"]
            # "age_at_diagnosis_btw": [0, 100]
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
            'sql': True,
            'CRDC_Study_GUID': True,
            'CRDC_Series_GUID': True,
            'CRDC_Instance_GUID': True,
            'gcs_bucket': True,
            'gcs_url': False,
            'aws_bucket': 'True',
            'aws_url': 'False',
            'page_size': 2000,
        }

         # Get a guid manifest of the cohort's instances
        response = client.post(f'{API_VERSION}/cohorts/manifest/preview',
                               query_string=query_string,
                               data=json.dumps(cohortSpec),
                               headers=headers)

        assert response.content_type == 'application/json'
        assert response.status_code == 400
        assert response.json['message'] == 'foo is not a valid filter.'



def test_guid(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

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
        'CRDC_Study_GUID': True,
        'CRDC_Series_GUID':True,
        'CRDC_Instance_GUID': True,
        'page_size': 2000,
    }

    query = gen_query(filters, query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

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


def test_url(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

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

    query = gen_query(filters, query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

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
    # assert {'GCS_URL': 'gs://public-datasets-idc/0190fe71-7144-40ae-a24c-c8d21a99317d/01210a30-8395-498c-905f-6667db67101a.dcm'} in json_manifest


def test_SOPInstanceUID(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

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

    query = gen_query(filters, query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]

    # Get a guid manifest of the cohort's instances
    response = client.post(f'{API_VERSION}/cohorts/manifest/preview',
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
    for bq_key in bq_data[0]:
        print(bq_key)
        api_key = next(api_key for api_key in json_manifest[0].keys() if bq_key.lower()==api_key.lower())
        assert (set(row[bq_key] for row in bq_data) == set(row[api_key] for row in json_manifest))
    # assert {'GCS_URL': 'gs://public-datasets-idc/dc19e1f0-63cf-422a-9742-c8c14de01370/de364433-4eaf-440e-b714-6c8b7cf3c613.dcm'} in json_manifest


def test_all(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

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
    query = gen_query(filters, query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]
    response = client.post(f'{API_VERSION}/cohorts/manifest/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

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


def test_all_paged(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')
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
        'page_size': 500
    }

    query = gen_query(filters, query_string)
    bq_data = [dict(row) for row in bq_client.query(query)]
    response = client.post(f'{API_VERSION}/cohorts/manifest/preview',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
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
            'next_page': next_page,
            'page_size': 500
        }

        response = client.get(f'{API_VERSION}/cohorts/manifest/nextPage',
                               query_string=query_string )
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
