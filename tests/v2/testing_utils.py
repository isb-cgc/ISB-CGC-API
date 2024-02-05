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

import json
from api.v2.schemas.filters import COHORT_FILTERS_SCHEMA
from api.v2.manifest_utils import process_special_fields, normalize_query_fields
from testing_branch import test_branch
from testing_config import dev_api_requester, API_URL, get_data, auth_header
import functools

levels = ["collections", "patients", "studies", "series", "instances"]

mimetype = ' application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

def _testMode(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if test_branch != "LOCAL":
            kwargs['client'] = dev_api_requester
        result = func(*args, **kwargs)
        return result
    return wrapper


def gen_query(manifestPreviewBody):
    schema = {
    }
    for filter, value in COHORT_FILTERS_SCHEMA['properties'].items():
        schema[filter.lower()] = value

    query = f"""
SELECT @fields
FROM `idc-dev-etl.idc_v{VERSION}_pub.dicom_pivot{'_v'+VERSION if VERSION < 15 else ''}` dicom_pivot
LEFT JOIN `idc-dev-etl.idc_v{VERSION}_pub.tcga_clinical_rel9` tcga_clinical
ON dicom_pivot.PatientID = tcga_clinical.case_barcode
WHERE @filters
GROUP BY @fields
ORDER BY @fields
            """
    # fields = ", ".join([key for key, value in query_string.items() if value in [True,'True'] and \
    #                     key not in ['sql', 'gcs_bucket', 'aws_bucket']])
    # if 'gcs_bucket' in query_string.keys():
    #     fields = f"{fields}, REGEXP_EXTRACT(gcs_url, r'^gs://([a-zA-Z0-9-]+)') gcs_bucket"
    # if 'aws_bucket' in query_string.keys():
    #     fields = f"{fields}, REGEXP_EXTRACT(aws_url, r'^s3://([a-zA-Z0-9-]+)') aws_bucket"
    filters = []
    for filter, value in manifestPreviewBody['cohort_def']['filters'].items():
        try:
            property = schema[filter.lower()]
            if property["items"]["type"] == "number":
                try:
                    suffix = filter.split('_')[-1]
                    op = filter.rsplit('_',1)[0]
                except:
                    suffix = ''
                    op = filter
                if suffix == '':
                    filters.append(f'({op} = {value[0]})' )
                elif suffix in ['lt', 'lte']:
                    filters.append( f'({op} <= {value[0]})')
                elif suffix in ['btw', 'ebtw', 'ebtwe', 'btwe']:
                    filters.append(f'({op} BETWEEN {value[0]} AND {value[1]})')
                elif suffix == 'lte':
                    filters.append(f'({op} <= {value[0]})')
                else:
                    filters.append(f'({op} < {value[0]})')
            else:
                # filters.append(f"{filter} in [{','.join([v for v in value])}]")
                if filter.lower() == 'collection_id':
                    for x, v in enumerate(value):
                        value[x] = v.lower().replace('-','_').replace(' ','_')
                filters.append(f"(lower({filter}) in {str(value).lower()})".replace('[', '(').replace(']',')'))
        except Exception as exc:
            print(f'{exc}')

    query = query.replace('@filters', '\nAND '.join(filters))

    # Now deal with 'special fields

    fields = manifestPreviewBody['fields']
    normalized_fields, special_fields, dummy = normalize_query_fields(fields)
    query = query.replace('@fields', ", ".join(normalized_fields))

    query_info = {
        'query': {
            'sql_string': query
        },
        'cohort_def': {
            'sql': query
        }
    }
    try:
        if eval(repr(manifestPreviewBody).lower().replace('true','True').replace('false','False'))['counts']:
            special_fields.append('counts')
    except:
        pass
    try:
        if eval(repr(manifestPreviewBody).lower().replace('true','True').replace('false','False'))['group_size']:
            special_fields.append('group_size')
    except:
        pass
    try:
        if 'studydate' in eval(repr(manifestPreviewBody['cohort_def']['filters']).lower()):
            special_fields.append('studydate')
    except:
        pass
    try:
        if 'studydescription' in eval(repr(manifestPreviewBody['cohort_def']['filters']).lower()):
            special_fields.append('studydescription')
    except:
        pass

    data = {
        'request_data': {
            'fields': fields
        }
    }
    if special_fields:
        query_info = process_special_fields(special_fields, query_info, data)
        query = query_info['query']['sql_string']
    return query

def pretty_print_cohortObjects(cohortObjects, indent=4):
    print(json.dumps(cohortObjects, sort_keys=True, indent=indent))

# This routine merges results from the /cohorts/{cohort_id} API with previously obtained results.
# It is intended for use when that API is used in a paged manner.
def merge(src, dst, level):
    keys = ["collection_id", "patient_id", "StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID"]
    for src_item in src:
        found = False
        for dst_item in dst:
            # if src_item["id"] == dst_item["id"]:
            if src_item[keys[level]] == dst_item[keys[level]]:
                if not len(levels) == level+1:
                    merge(src_item[levels[level+1]], dst_item[levels[level+1]], level+1)
                found = True
                break
        if not found:
            dst.append(src_item)

 # Utility to create a "standard" cohort for testing
def create_cohort(client):
    # Define the filters
    filters = {
        "collection_id": ["tcga_luad", "tcga_kirc"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"],
        "age_at_diagnosis_btw": [1, 100],
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post(f'{API_URL}/cohorts',
                           data=json.dumps(cohortSpec),
                           headers=headers | auth_header)
    assert response.status_code == 200
    cohortResponse = get_data(response)['cohort_properties']

    return cohortResponse, cohortSpec


# Create a cohort with filter as expected by the test_get_cohort_xxx() functions
def create_cohort_for_test_get_cohort_xxx(client, filters=None):
    # Create a cohort to test against
    if not filters:
        filters = {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "age_at_diagnosis_btw": [1, 100],
            "race": ["WHITE"]
        }

    cohortSpec = {"name": "testcohort",
              "description": "Test description",
              "filters": filters}

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post(f'{API_URL}/cohorts',
                           data=json.dumps(cohortSpec),
                           headers=headers | auth_header)
    assert response.status_code == 200
    cohortResponse = get_data(response)['cohort_properties']
    id = cohortResponse['cohort_id']
    return (id, cohortSpec)


# Utility to delete an existing cohort
def delete_cohort(client, id):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    headers = headers | auth_header
    response = client.delete(f"{API_URL}/cohorts/{id}/",
                   headers=headers )
    assert response.status_code == 200

def current_version(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.get(f'{API_URL}/versions')
    data = get_data(response)['versions']
    current = str(max([float(v['idc_data_version']) for v in data]))
    return current




