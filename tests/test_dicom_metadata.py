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


def test_query_metadata(client, app):

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'page_size': 5000
    }

    response = client.get('v1/dicomMetadata',
                            query_string = query_string,
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    totalFound = response.json['query_results']['totalFound']
    all_query_rows = response.json['query_results']['json']
    totalRowsReturned = response.json['query_results']['rowsReturned']

    next_page = response.json['next_page']
    assert next_page

    while next_page and totalRowsReturned < 50000:
        query_string = {
            'next_page': next_page,
            'page_size': 5000
        }

        # Get the list of objects in the cohort
        response = client.get('v1/dicomMetadata/nextPage',
                              query_string=query_string,
                              headers=headers)
        assert response.content_type == 'application/json'
        assert response.status_code == 200
        all_query_rows.extend(response.json['query_results']['json'])
        totalRowsReturned += response.json['query_results']['rowsReturned']
        next_page = response.json['next_page']

    assert totalRowsReturned == 50000