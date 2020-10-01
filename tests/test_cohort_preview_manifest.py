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

def test_cohort_preview_manifest(client, app):

    filterSet = {
        "idc_data_version": "",
        "filters": {
            "collection_id": ["tcga_read"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"]}}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'access_class': 'url',
    }

    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    manifest = response.json['manifest']
    assert manifest['accessMethods']['type'] == 'gs'
    assert manifest['accessMethods']['region'] == 'us'
    assert len(manifest['accessMethods']['urls']) == 1638
    assert len(manifest['accessMethods']['dois']) == 0
    assert manifest['accessMethods']['totalFound'] == 1638
    assert manifest['accessMethods']['rowsReturned'] ==1638
    assert manifest['accessMethods']['next_page'] == None


    assert 'gs://idc-tcia-tcga-read/dicom/1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508/1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631/1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597.dcm#1592638257658431' \
        in manifest['accessMethods']['urls']

    query_string = {
        'access_class': 'doi',
    }

    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    manifest = response.json['manifest']
    assert manifest['accessMethods']['type'] == 'gs'
    assert manifest['accessMethods']['region'] == 'us'
    assert len(manifest['accessMethods']['urls']) == 0
    assert len(manifest['accessMethods']['dois']) == 1638
    assert manifest['accessMethods']['totalFound'] == 1638
    assert manifest['accessMethods']['rowsReturned'] ==1638
    assert manifest['accessMethods']['next_page'] == None


def test_get_cohort_preview_manifest_paged_doi(client, app):

    filterSet = {
        "idc_data_version": "",
        "filters": {
            "collection_id": ["tcga_luad"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"]}}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'access_class': 'doi',
    }

    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.status_code == 200
    manifest = response.json['manifest']

    accessMethods = manifest['accessMethods']
    assert accessMethods['type'] == 'gs'
    assert accessMethods['region'] == 'us'
    assert len(accessMethods['urls']) == 0
    assert len(accessMethods['dois']) == 5000
    assert accessMethods['totalFound'] == 21940
    assert accessMethods['rowsReturned'] ==5000

    job_reference = accessMethods['job_reference']
    next_page = accessMethods['next_page']
    assert job_reference
    assert next_page

    #Now get the remaining pages
    totaldois= accessMethods['dois']
    totalRowsReturned = accessMethods['rowsReturned']

    while next_page:
        query_string = {
            'access_class': 'doi',
            'job_reference': job_reference,
            'next_page': next_page
        }

        # Get the list of objects in the cohort
        response = client.post('v1/cohorts/preview/manifest',
                               query_string=query_string,
                               data=json.dumps(cohortSpec),
                               headers=headers)

        assert response.content_type == 'application/json'
        assert response.status_code == 200
        manifest = response.json['manifest']

        accessMethods = manifest['accessMethods']
        rowsReturned = accessMethods["rowsReturned"]
        totalRowsReturned += rowsReturned
        dois = accessMethods["dois"]
        totaldois.extend(dois)
        job_reference = accessMethods['job_reference']
        next_page = accessMethods['next_page']

    assert 'dg.4DFC/0009e98e-bca2-4a68-ada1-62e0a8b2dbaf' in totaldois
    assert totalRowsReturned == accessMethods['totalFound']
    assert accessMethods['totalFound'] == len(set(totaldois))


def test_get_cohort_manifest_paged_url(client, app):

    filterSet = {
        "idc_data_version": "",
        "filters": {
            "collection_id": ["tcga_luad"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"]}}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    query_string = {
        'access_class': 'url',
    }

    response = client.post('v1/cohorts/preview/manifest',
                            query_string = query_string,
                            data = json.dumps(cohortSpec),
                            headers=headers)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    manifest = response.json['manifest']

    accessMethods = manifest['accessMethods']
    assert accessMethods['type'] == 'gs'
    assert accessMethods['region'] == 'us'
    assert len(accessMethods['urls']) == 5000
    assert len(accessMethods['dois']) == 0
    assert accessMethods['totalFound'] == 21940
    assert accessMethods['rowsReturned'] ==5000

    job_reference = accessMethods['job_reference']
    next_page = accessMethods['next_page']
    assert job_reference
    assert next_page

    #Now get the remaining pages
    totalurls= accessMethods['urls']
    totalRowsReturned = accessMethods['rowsReturned']

    while next_page:
        query_string = {
            'access_class': 'url',
            'job_reference': job_reference,
            'next_page': next_page
        }

        # Get the list of objects in the cohort
        response = client.post('v1/cohorts/preview/manifest',
                               query_string=query_string,
                               data=json.dumps(cohortSpec),
                               headers=headers)

        assert response.content_type == 'application/json'
        assert response.status_code == 200
        manifest = response.json['manifest']

        accessMethods = manifest['accessMethods']
        rowsReturned = accessMethods["rowsReturned"]
        totalRowsReturned += rowsReturned
        urls = accessMethods["urls"]
        totalurls.extend(urls)
        job_reference = accessMethods['job_reference']
        next_page = accessMethods['next_page']

    assert 'gs://idc-tcia-tcga-luad/dicom/1.3.6.1.4.1.14519.5.2.1.3983.9002.107656215131152599944682699489/1.3.6.1.4.1.14519.5.2.1.3983.9002.169653067901690682811265889199/1.3.6.1.4.1.14519.5.2.1.3983.9002.139964879860094005134659511427.dcm#1592637570041744' \
        in totalurls
    assert totalRowsReturned == accessMethods['totalFound']
    assert accessMethods['totalFound'] == len(set(totalurls))
