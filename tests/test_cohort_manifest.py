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


from .cohort_utils import pretty_print_cohortObjects, merge, create_cohort, create_cohort_for_test_get_cohort_xxx, create_big_cohort_for_test_get_cohort_xxx, delete_cohort

def test_get_cohort_manifest_doi(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'access_method': 'doi',
    }

    # Get a doi manifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']
    job_reference = response.json['job_reference']
    next_page = response.json['next_page']

    assert cohort['cohort_id']==id

    assert manifest['url_access_type'] == 'gs'
    assert manifest['url_region'] == 'us'
    assert len(manifest['urls']) == 0
    assert len(manifest['dois']) == 1638
    assert manifest['totalFound'] == 1638
    assert manifest['rowsReturned'] ==1638
    assert next_page == None

    query_string = {
        'access_method': 'url',
    }

def test_get_cohort_manifest_url(client, app):

    (id, filterSet) = create_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'access_method': 'url',
    }

    # Get a urlmanifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']
    job_reference = response.json['job_reference']
    next_page = response.json['next_page']

    assert cohort['cohort_id']==id

    assert manifest['url_access_type'] == 'gs'
    assert manifest['url_region'] == 'us'
    assert len(manifest['urls']) == 1638
    assert len(manifest['dois']) == 0
    assert manifest['totalFound'] == 1638
    assert manifest['rowsReturned'] ==1638
    assert next_page == None

    assert 'gs://idc-tcia-tcga-read/dicom/1.3.6.1.4.1.14519.5.2.1.3671.4018.768291480177931556369061239508/1.3.6.1.4.1.14519.5.2.1.3671.4018.183714953600569164837490663631/1.3.6.1.4.1.14519.5.2.1.3671.4018.101814896314793708382026281597.dcm#1592638257658431' \
        in manifest['urls']

    delete_cohort(client, id)

def test_get_manifest_paged_doi(client, app):

    (id, filterSet) = create_big_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'access_method': 'doi',
        'page_size': 5000
    }

    # Get a manifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']
    job_reference = response.json['job_reference']
    next_page = response.json['next_page']

    assert cohort['cohort_id']==id

    assert manifest['url_access_type'] == 'gs'
    assert manifest['url_region'] == 'us'
    assert len(manifest['urls']) == 0
    assert len(manifest['dois']) == 5000
    assert manifest['totalFound'] == 21940
    assert manifest['rowsReturned'] ==5000

    assert job_reference
    assert next_page

    #Now get the remaining pages
    totaldois= manifest['dois']
    totalRowsReturned = manifest['rowsReturned']

    while next_page:
        query_string = {
            'access_method': 'doi',
            'job_reference': job_reference,
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
        job_reference = response.json['job_reference']
        next_page = response.json['next_page']

        rowsReturned = manifest["rowsReturned"]
        totalRowsReturned += rowsReturned
        dois = manifest["dois"]
        totaldois.extend(dois)

    assert 'dg.4DFC/0009e98e-bca2-4a68-ada1-62e0a8b2dbaf' in totaldois
    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(set(totaldois))


    delete_cohort(client, id)


def test_get_cohort_manifest_paged_url(client, app):

    (id, filterSet) = create_big_cohort_for_test_get_cohort_xxx(client)

    query_string = {
        'access_method': 'url',
        'page_size': 5000
    }

    # Get a manifest of the cohort's instances
    response = client.get("{}/{}/manifest/".format('v1/cohorts', id),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = response.json['cohort']
    manifest = response.json['manifest']
    job_reference = response.json['job_reference']
    next_page = response.json['next_page']

    assert cohort['cohort_id']==id

    assert manifest['url_access_type'] == 'gs'
    assert manifest['url_region'] == 'us'
    assert len(manifest['urls']) == 5000
    assert len(manifest['dois']) == 0
    assert manifest['totalFound'] == 21940
    assert manifest['rowsReturned'] ==5000

    assert job_reference
    assert next_page

    #Now get the remaining pages
    totalurls= manifest['urls']
    totalRowsReturned = manifest['rowsReturned']

    while next_page:
        query_string = {
            'access_method': 'url',
            'job_reference': job_reference,
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
        job_reference = response.json['job_reference']
        next_page = response.json['next_page']

        rowsReturned = manifest["rowsReturned"]
        totalRowsReturned += rowsReturned
        urls = manifest["urls"]
        totalurls.extend(urls)

    assert 'gs://idc-tcia-tcga-luad/dicom/1.3.6.1.4.1.14519.5.2.1.3983.9002.107656215131152599944682699489/1.3.6.1.4.1.14519.5.2.1.3983.9002.169653067901690682811265889199/1.3.6.1.4.1.14519.5.2.1.3983.9002.139964879860094005134659511427.dcm#1592637570041744' \
        in totalurls
    assert totalRowsReturned == manifest['totalFound']
    assert manifest['totalFound'] == len(set(totalurls))


    delete_cohort(client, id)



