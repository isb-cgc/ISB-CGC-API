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
from google.cloud import bigquery

def test_basic(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters= {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "Race": ["WHITE"]
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    fields =  ['StudyInstanceUID', 'modality']

    queryPreviewBody = {"cohort_def": cohortSpec,
                        "fields": fields}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'sql': False,
        'page_Size': 2000,
    }

    query = gen_query(filters, {field: "True" for field in fields})
    bq_data = [dict(row) for row in bq_client.query(query)]

    response = client.post(f'{API_VERSION}/cohorts/query/preview',
                            query_string = query_string,
                            data = json.dumps(queryPreviewBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    info = response.json
    cohort_def = info['cohort_def']
    assert cohort_def['name'] == cohortSpec['name']
    assert cohort_def['description'] == cohortSpec['description']
    assert set(filter.lower() for filter in cohort_def['filterSet']['filters']) == \
           set(filter.lower() for filter in cohortSpec['filters'])

    assert response.json['query_results']['rowsReturned'] == len(bq_data)
    assert response.json['query_results']['totalFound'] == len(bq_data)

    assert response.json['next_page'] == ""

    query_results = info['query_results']['json']
    assert len(query_results) ==  response.json['query_results']['rowsReturned']
    for bq_key in bq_data[0]:
        api_key = next(api_key for api_key in query_results[0].keys() if bq_key.lower()==api_key.lower())
        assert (set(row[bq_key] for row in bq_data) == set(row[api_key] for row in query_results))


def test_basic2(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    fields =  ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'Modality']

    queryPreviewBody = {"cohort_def": cohortSpec,
                        "fields": fields}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'sql': False,
        'page_size': 2000,
    }

    query = gen_query(filters, {field: "True" for field in fields})
    bq_data = [dict(row) for row in bq_client.query(query)]

    response = client.post(f'{API_VERSION}/cohorts/query/preview',
                            query_string = query_string,
                            data = json.dumps(queryPreviewBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    info = response.json
    cohort_def = info['cohort_def']
    assert cohort_def['name'] == cohortSpec['name']
    assert cohort_def['description'] == cohortSpec['description']
    assert cohort_def['filterSet']['filters'] == cohortSpec['filters']

    assert response.json['query_results']['rowsReturned'] == len(bq_data)
    assert response.json['query_results']['totalFound'] == len(bq_data)

    assert response.json['next_page'] == ""

    query_results = info['query_results']['json']
    assert len(query_results) ==  response.json['query_results']['rowsReturned']
    for bq_key in bq_data[0]:
        api_key = next(api_key for api_key in query_results[0].keys() if bq_key.lower()==api_key.lower())
        assert (set(row[bq_key] for row in bq_data) == set(row[api_key] for row in query_results))
    # assert {'Modality': 'CT', 'SOPInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597', \
    #         'SeriesInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631', \
    #         'StudyInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508'} \
    #     in query_results


def test_paged(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    fields = ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'Modality']

    queryPreviewBody = {"cohort_def": cohortSpec,
                        "fields": fields}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'sql': False,
        'page_size': 500,
    }

    query = gen_query(filters, {field: "True" for field in fields})
    bq_data = [dict(row) for row in bq_client.query(query)]

    response = client.post(f'{API_VERSION}/cohorts/query/preview',
                            query_string = query_string,
                            data = json.dumps(queryPreviewBody),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    info = response.json
    cohort_def = info['cohort_def']
    assert cohort_def['name'] == cohortSpec['name']
    assert cohort_def['description'] == cohortSpec['description']
    assert cohort_def['filterSet']['filters'] == cohortSpec['filters']

    totalRowsReturned = response.json['query_results']['rowsReturned']
    assert response.json['query_results']['totalFound'] == len(bq_data)

    assert response.json['next_page']

    query_results = info['query_results']['json']
    assert len(query_results) ==  response.json['query_results']['rowsReturned']
    while response.json['next_page']:
        query_string = {
            # 'sql': False,
            'page_size': 500,
            'next_page': response.json['next_page']
        }

        response = client.get(f'{API_VERSION}/cohorts/query/nextPage',
                               query_string=query_string
                              )
                               # data=json.dumps(queryPreviewBody),
                               # headers=headers)

        assert response.content_type == 'application/json'
        assert response.status_code == 200
        info = response.json
        totalRowsReturned += response.json['query_results']['rowsReturned']

        query_results.extend(info['query_results']['json'])

    assert totalRowsReturned == response.json['query_results']['totalFound']
    assert len(query_results) == response.json['query_results']['totalFound']
    for bq_key in bq_data[0]:
        api_key = next(api_key for api_key in query_results[0].keys() if bq_key.lower()==api_key.lower())
        assert (set(row[bq_key] for row in bq_data) == set(row[api_key] for row in query_results))

    # assert {'Modality': 'CT', 'SOPInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597', \
    #         'SeriesInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631', \
    #         'StudyInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508'} \
    #     in query_results