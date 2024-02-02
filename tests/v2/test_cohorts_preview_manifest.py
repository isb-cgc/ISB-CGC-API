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

from testing_branch import test_branch
from testing_config import API_URL, get_data, VERSION
import json
import datetime
from testing_utils import _testMode
from google.cloud import bigquery


@_testMode
def test_invalid_params(client, app):
    filters = {
        "age_at_diagnosis_btw": [65.1, 75],
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
        "cohort_def": cohort_def,
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
    assert get_data(response)['message'] == '65.1 is not of type \'integer\'; Failed validating type in schema [\'properties\'],[\'age_at_diagnosis_btw\'],[\'items\'] on instance [\'age_at_diagnosis_btw\'],[0]'

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
        "collection_id": ["TCGA-read"],
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
        'age_at_diagnosis',
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


# Test that the generated SQL is correct. Iterate over ranged filters
@_testMode
def test_sql_ranged_integer(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    attribute = "age_at_diagnosis"
    ops = {
        'eq': {
            "values": [65],
            "clause": f"tcga_clinical_rel9.{attribute} = 65"
        },
        'lt': {
            "values": [75],
            "clause": f"tcga_clinical_rel9.{attribute} < 75"
        },
        'lte': {
            "values": [75],
            "clause": f"tcga_clinical_rel9.{attribute} <= 75"
        },
        'gt': {
            "values": [100],
            "clause": f"tcga_clinical_rel9.{attribute} > 100"
        },
        'gte': {
            "values": [100],
            "clause": f"tcga_clinical_rel9.{attribute} >= 100"
        },
        'ebtw': {
            "values": [65, 75],
            "clause": f"tcga_clinical_rel9.{attribute} >= 65 AND tcga_clinical_rel9.{attribute} < 75"
        },
        'btw': {
            "values": [65, 75],
            "clause": f"tcga_clinical_rel9.{attribute} > 65 AND tcga_clinical_rel9.{attribute} < 75"
        },
        'btwe': {
            "values": [65, 75],
            "clause": f"tcga_clinical_rel9.{attribute} > 65 AND tcga_clinical_rel9.{attribute} <= 75"
        },
        'ebtwe': {
            "values": [65, 75],
            "clause": f"tcga_clinical_rel9.{attribute} BETWEEN 65 AND 75"
        },
    }
    for op, val in ops.items():
        print(f"Testing operand {op} with values {val}")
        pivot = f'bigquery-public-data.idc_v{VERSION}.dicom_pivot' if test_branch=='PROD' else f'idc-dev-etl.idc_v{VERSION}_pub.dicom_pivot'
        expected_sql = f"""\n            #standardSQL\n    \n        SELECT dicom_pivot.collection_id,dicom_pivot.crdc_study_uuid,dicom_pivot.crdc_series_uuid,dicom_pivot.crdc_instance_uuid,dicom_pivot.gcs_bucket,dicom_pivot.gcs_url,dicom_pivot.aws_bucket,dicom_pivot.aws_url,tcga_clinical_rel9.age_at_diagnosis\n        FROM `{pivot}` dicom_pivot \n        \n        LEFT JOIN `bigquery-public-data.idc_v4.tcga_clinical_rel9` tcga_clinical_rel9\n        ON dicom_pivot.PatientID = tcga_clinical_rel9.case_barcode\n    \n        WHERE ((dicom_pivot.collection_id = "tcga_read")) AND ((LOWER(dicom_pivot.Modality) IN UNNEST(["ct", "mr"]))) AND ((({val['clause']})) AND ((tcga_clinical_rel9.race = "WHITE")) OR tcga_clinical_rel9.case_barcode IS NULL)\n        \n        GROUP BY dicom_pivot.collection_id, dicom_pivot.crdc_study_uuid, dicom_pivot.crdc_series_uuid, dicom_pivot.crdc_instance_uuid, tcga_clinical_rel9.age_at_diagnosis, dicom_pivot.gcs_bucket, dicom_pivot.gcs_url, dicom_pivot.aws_bucket, dicom_pivot.aws_url\n        ORDER BY dicom_pivot.collection_id ASC, dicom_pivot.crdc_study_uuid ASC, dicom_pivot.crdc_series_uuid ASC, dicom_pivot.crdc_instance_uuid ASC, tcga_clinical_rel9.age_at_diagnosis ASC, dicom_pivot.gcs_bucket ASC, dicom_pivot.gcs_url ASC, dicom_pivot.aws_bucket ASC, dicom_pivot.aws_url ASC\n        \n        \n    """

        filters = {
            "collection_id": ["TCGA-read"],
            "Modality": ["ct", "mR"],
            f'{attribute}_{op}': val['values'],
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
            'age_at_diagnosis',
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
        assert cohort_def['sql'] == expected_sql



# Test that the generated SQL is correct. Iterate over ranged filters
@_testMode
def test_sql_ranged_number(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    attribute = "bmi"
    ops = {
        'eq': {
            "values": [65.1],
            "clause": f"tcga_clinical_rel9.{attribute} = 65.1"
        },
        'lt': {
            "values": [75.1],
            "clause": f"tcga_clinical_rel9.{attribute} < 75.1"
        },
        'lte': {
            "values": [75.1],
            "clause": f"tcga_clinical_rel9.{attribute} <= 75.1"
        },
        'gt': {
            "values": [100.1],
            "clause": f"tcga_clinical_rel9.{attribute} > 100.1"
        },
        'gte': {
            "values": [100.1],
            "clause": f"tcga_clinical_rel9.{attribute} >= 100.1"
        },
        'ebtw': {
            "values": [65.1, 75.1],
            "clause": f"tcga_clinical_rel9.{attribute} >= 65.1 AND tcga_clinical_rel9.{attribute} < 75.1"
        },
        'btw': {
            "values": [65.1, 75.1],
            "clause": f"tcga_clinical_rel9.{attribute} > 65.1 AND tcga_clinical_rel9.{attribute} < 75.1"
        },
        'btwe': {
            "values": [65.1, 75.1],
            "clause": f"tcga_clinical_rel9.{attribute} > 65.1 AND tcga_clinical_rel9.{attribute} <= 75.1"
        },
        'ebtwe': {
            "values": [65.1, 75.1],
            "clause": f"tcga_clinical_rel9.{attribute} BETWEEN 65.1 AND 75.1"
        },
    }
    for op, val in ops.items():
        print(f"Testing operand {op} with values {val}")
        pivot = f'bigquery-public-data.idc_v{VERSION}.dicom_pivot' if test_branch=="PROD" else f'idc-dev-etl.idc_v{VERSION}_pub.dicom_pivot'
        expected_sql = f"""\n            #standardSQL\n    \n        SELECT dicom_pivot.collection_id,dicom_pivot.crdc_study_uuid,dicom_pivot.crdc_series_uuid,dicom_pivot.crdc_instance_uuid,dicom_pivot.gcs_bucket,dicom_pivot.gcs_url,dicom_pivot.aws_bucket,dicom_pivot.aws_url,tcga_clinical_rel9.age_at_diagnosis\n        FROM `{pivot}` dicom_pivot \n        \n        LEFT JOIN `bigquery-public-data.idc_v4.tcga_clinical_rel9` tcga_clinical_rel9\n        ON dicom_pivot.PatientID = tcga_clinical_rel9.case_barcode\n    \n        WHERE ((dicom_pivot.collection_id = "tcga_read")) AND ((LOWER(dicom_pivot.Modality) IN UNNEST(["ct", "mr"]))) AND ((({val['clause']})) AND ((tcga_clinical_rel9.race = "WHITE")) OR tcga_clinical_rel9.case_barcode IS NULL)\n        \n        GROUP BY dicom_pivot.collection_id, dicom_pivot.crdc_study_uuid, dicom_pivot.crdc_series_uuid, dicom_pivot.crdc_instance_uuid, tcga_clinical_rel9.age_at_diagnosis, dicom_pivot.gcs_bucket, dicom_pivot.gcs_url, dicom_pivot.aws_bucket, dicom_pivot.aws_url\n        ORDER BY dicom_pivot.collection_id ASC, dicom_pivot.crdc_study_uuid ASC, dicom_pivot.crdc_series_uuid ASC, dicom_pivot.crdc_instance_uuid ASC, tcga_clinical_rel9.age_at_diagnosis ASC, dicom_pivot.gcs_bucket ASC, dicom_pivot.gcs_url ASC, dicom_pivot.aws_bucket ASC, dicom_pivot.aws_url ASC\n        \n        \n    """

        filters = {
            "collection_id": ["TCGA-read"],
            "Modality": ["ct", "mR"],
            f'{attribute}_{op}': val['values'],
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
            'age_at_diagnosis',
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
        assert cohort_def['sql'] == expected_sql



@_testMode
def test_special_fields(client, app):
    bq_client = bigquery.Client(project='idc-dev-etl')

    filters = {
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

        if test_branch != "LOCAL":
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
