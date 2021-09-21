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

def test_basic(client, app):

    filters= {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    queryFields = {"fields": ['StudyInstanceUID', 'Modality']}

    queryPreviewBody = {"cohort_def": cohortSpec,
                        "queryFields": queryFields}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'sql': False,
        'page_size': 2000,
    }

    response = client.post('v1/cohorts/query/preview',
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

    assert response.json['query_results']['rowsReturned'] == 3
    assert response.json['query_results']['totalFound'] == 3

    assert response.json['next_page'] == ""

    query_results = info['query_results']['json']
    assert len(query_results) ==  response.json['query_results']['rowsReturned']
    assert {'Modality': 'CT', 'StudyInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508'} \
        in query_results

def test_basic2(client, app):

    filters = {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    queryFields = {"fields": ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'Modality']}

    queryPreviewBody = {"cohort_def": cohortSpec,
                        "queryFields": queryFields}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'sql': False,
        'page_size': 2000,
    }

    response = client.post('v1/cohorts/query/preview',
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

    assert response.json['query_results']['rowsReturned'] == 1638
    assert response.json['query_results']['totalFound'] == 1638

    assert response.json['next_page'] == ""

    query_results = info['query_results']['json']
    assert len(query_results) ==  response.json['query_results']['rowsReturned']
    assert {'Modality': 'CT', 'SOPInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597', \
            'SeriesInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631', \
            'StudyInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508'} \
        in query_results


def test_paged(client, app):

    filters = {
        "collection_id": ["tcga_read"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    queryFields = {"fields": ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'Modality']}

    queryPreviewBody = {"cohort_def": cohortSpec,
                        "queryFields": queryFields}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'sql': False,
        'page_size': 500,
    }

    response = client.post('v1/cohorts/query/preview',
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
    assert response.json['query_results']['totalFound'] == 1638

    assert response.json['next_page']

    query_results = info['query_results']['json']
    assert len(query_results) ==  response.json['query_results']['rowsReturned']
    assert {'Modality': 'CT', 'SOPInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597', \
            'SeriesInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631', \
            'StudyInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508'} \
        in query_results

    while response.json['next_page']:
        query_string = {
            # 'sql': False,
            'page_size': 500,
            'next_page': response.json['next_page']
        }

        response = client.get('v1/cohorts/query/nextPage',
                               query_string=query_string,
                               data=json.dumps(queryPreviewBody),
                               headers=headers)

        assert response.content_type == 'application/json'
        assert response.status_code == 200
        info = response.json
        totalRowsReturned += response.json['query_results']['rowsReturned']

        query_results.extend(info['query_results']['json'])

    assert totalRowsReturned == response.json['query_results']['totalFound']
    assert len(query_results) == response.json['query_results']['totalFound']

    assert {'Modality': 'CT', 'SOPInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597', \
            'SeriesInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631', \
            'StudyInstanceUID': '1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508'} \
        in query_results