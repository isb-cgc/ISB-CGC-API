#
# Copyright 2015-2019, Institute for Systems Biology
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
from __future__ import absolute_import

import logging
import re
import json
import requests
from api.schemas.filters import COHORT_FILTERS_SCHEMA

from api.auth import get_auth
from cryptography.fernet import Fernet, InvalidToken

import settings
from google_helpers.bigquery.bq_support import BigQuerySupport
from jsonschema import validate as schema_validate, ValidationError

logger = logging.getLogger(settings.LOGGER_NAME)
logger.setLevel(settings.LOG_LEVEL)


CRDC_GUID_PREFIX='dg.4DFC'

logger = logging.getLogger('main_logger')
BLACKLIST_RE = settings.BLACKLIST_RE

cipher_suite = Fernet(settings.PAGE_TOKEN_KEY)

default_manifest_params = {
    "page_size": 1000,
    "sql": False,
    "collection_id": False,
    "PatientID": False,
    "StudyInstanceUID": False,
    "SeriesInstanceUID": False,
    "SOPInstanceUID": False,
    "source_DOI": False,
    "crdc_study_uuid": True,
    "crdc_series_uuid": False,
    "crdc_instance_uuid": False,
    "gcs_bucket": False,
    "gcs_url": False,
    "aws_bucket": False,
    "aws_url": False,
}

lowered_manifest_params = {key.lower(): key for key in default_manifest_params}

default_query_params = {
    "page_size": 1000,
    "sql": False,
}
lowered_query_params = {key.lower(): key for key in default_query_params}


def encrypt_pageToken(email, jobReference, next_page, op):
    # cipher_suite = Fernet(settings.PAGE_TOKEN_KEY)
    jobDescription = dict(
        email = email,
        jobReference = jobReference,
        next_page = next_page,
        op = op
    )
    plain_jobDescription = json.dumps(jobDescription).encode()

    cipher_jobReference = cipher_suite.encrypt(plain_jobDescription).decode()

    return cipher_jobReference


def decrypt_pageToken(email, cipher_jobReference, op):
    # cipher_suite = Fernet(settings.PAGE_TOKEN_KEY)
    try:
        plain_jobDescription = cipher_suite.decrypt(cipher_jobReference.encode())
        jobDescription = json.loads(plain_jobDescription.decode())
        if jobDescription["email"] != email:
            # Caller's email doesn't match what was encrypted
            logger.error("Caller's email, {}, doesn't match what was encrypted: {}".format(
                email, jobDescription['email']))
            return {}
        elif jobDescription["op"] != op:
            # Caller's email doesn't match what was encrypted
            logger.error("Incorrect next_page endpoint for next_page token".format(
                email, jobDescription['email']))
            return {}
        else:
            jobDescription.pop('email')
            jobDescription.pop('op')
            return jobDescription
    except InvalidToken:
        logger.error("Could not decrypt token: {}".format(cipher_jobReference))
        return {}


def submit_BQ_job(sql_string, params):
    results = BigQuerySupport.execute_query_and_fetch_results(sql_string, params, no_results=True)
    logger.debug("submit_BQ_job() results: %s", results)
    return results


# Deal with casing issues in filterset, converting to normalized values
def normalize_filterset(filterset):
    corrected_filters = {}
    lowered_filters = {key.lower(): key for key in COHORT_FILTERS_SCHEMA['properties'].keys()}
    for filter, value in filterset.items():
        if filter.lower() in lowered_filters:
            corrected_filters[lowered_filters[filter.lower()]] = value
        else:
            return (filterset, dict(
                message=f'{filter} is not a valid filter.',
                code=400
            )
                    )
    return corrected_filters, {}


def validate_cohort_definition(cohort_def):
    try:
        if 'name' not in cohort_def:
            return (cohort_def, dict(
                        message='A name was not provided for this cohort.',
                        code=400
                        )
                    )
        if 'filters' not in cohort_def:
            return (cohort_def, dict(
                        message='No filters were provided; ensure that the request body contains a \'filters\' property.',
                        code=400
                        )
                    )

        # Replace submitted filter IDs normalized filter IDs
        cohort_def['filters'], filter_info = normalize_filterset(cohort_def['filters'])
        if 'message' in filter_info:
            return(cohort_def, filter_info)
        # Validate the filterset
        schema_validate(cohort_def['filters'], COHORT_FILTERS_SCHEMA)

        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match = blacklist.search(str(cohort_def['name']))

        if not match and 'description' in cohort_def:
            match = blacklist.search(str(cohort_def['description']))

        if match:
            return (cohort_def, dict(
                            message="Your cohort's name or description contains invalid characters; " +
                                    "please edit them and resubmit. [Saw {}]".format(str(match)),
                            code=400
                        )
                    )
        return (cohort_def, {})
    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        manifest_info = dict(
            message= f'[WARNING] {e}',
            code = 400)
        return {}, manifest_info


def validate_query_parameters(request, default_params, lowered_params):

    corrected_params = default_params
    params =  [key for key in corrected_params]

    # Correct casing errors in param names
    for param, value in request.args.items():
        if param.lower() in lowered_params:
            corrected_params[lowered_params[param.lower()]] = value
        else:
            param_info =  dict(
                message = f"{param} is an invalid param.",
                code = 400
            )
            return params, param_info
        
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    for param, value in corrected_params.items():
        # Verify that params have acceptable values
        # Parameter pages must have an integer value or be
        # convertible to an integer
        if param == 'page_size':
            if not value in ["", None]:
                try:
                    corrected_params[param] = int(value)
                except:
                    manifest_info = dict(
                        message=f"Parameter pages must be Null or an empty string" +
                            "or an integer or convertibe to an integer",
                        code=400
                    )
                    return [], manifest_info
        else:
            # Other params must have values that are convertible to a boolean
            if value in [True, "True"]:
                corrected_params[param] = True
            elif value in [False, "False"]:
                corrected_params[param] = False
            else:
                manifest_info = dict(
                    message=f'Parameter {param} must be on of [True", "True", False, "False"]',
                    code=400
                )
                return [], manifest_info

    # There must be at least one param that selects a column
    for param in corrected_params:
        if param in params[1:]:
            return corrected_params, {}

    manifest_info = dict(
        message=f'At least one query parameter must be True.',
        code=400
    )
    return [], manifest_info


def get_manifest(request, func, url, data=None): #, user=None):
    next_page = ""
    try:
        query_params, error_info = validate_query_parameters(request, \
                 default_manifest_params.copy(), lowered_manifest_params)
        if error_info:
            return error_info
        # if user:
        #     query_params['email'] = user

        auth = get_auth()
        if func == requests.post:
            results = func(url, params=query_params, json=data, headers=auth)
        else:
            results = func(url, params=query_params, json=data, headers=auth)

        manifest_info = results.json()

        if "message" in manifest_info:
            return manifest_info

        # Temporary workaround to support aws_bucket
        if 'aws_bucket' in query_params and query_params['aws_bucket'] == True:
            manifest_info['query']['sql_string'] = \
            manifest_info['query']['sql_string'].replace('SELECT', 'SELECT dicom_pivot.aws_bucket,')
            manifest_info['query']['sql_string'] = \
            manifest_info['query']['sql_string'].replace('GROUP BY', 'GROUP BY dicom_pivot.aws_bucket,')


        # We now have SQL that will generate the request manifest
        # Start the BQ job, but don't get any data results, just the job info.
        job_status = submit_BQ_job(manifest_info['query']['sql_string'],
                                    manifest_info['query']['params'])
        jobReference = job_status['jobReference']

        # Decide how to proceed depending on job status (DONE, RUNNING, ERRORS)
        user = data["email"]
        manifest_info = is_job_done(job_status, manifest_info, jobReference, user, 'manifest')

        if "message" in manifest_info:
            return manifest_info

        manifest_info, next_page = get_manifest_job_results(manifest_info,
                    query_params['page_size'], jobReference, next_page)
        if next_page:
            cipher_pageToken = encrypt_pageToken(user, jobReference, next_page, 'manifest')
        else:
            cipher_pageToken = ""
        manifest_info['next_page'] = cipher_pageToken

    except Exception as e:
        logger.exception(e)
        manifest_info = dict(
            message='[ERROR] get_manifest(): Error trying to preview a cohort',
            code=400)

    return manifest_info


def get_manifest_nextpage(request, user):
    manifest_info = {}
    page_params = {
        "page_size": 1000,
        "next_page": ""
    }
    for param, value in request.args.items():
        if param.lower() == 'page_size':
            try:
                page_params['page_size'] = int(value)
            except:
                manifest_info = dict(
                    message="Invalid page_size",
                    code=400
                )
                return manifest_info
        elif param.lower() == 'next_page':
            page_params['next_page'] = value
        else:
            manifest_info = dict(
                message=f"Invalid query parameter {param}",
                code=400
            )
            return manifest_info

    try:
        if not page_params['next_page'] in ["", None]:
            # We have a non-empty next_page token
            jobDescription = decrypt_pageToken(user, page_params['next_page'], 'manifest')
            if jobDescription == {}:
                manifest_info = dict(
                    message="Invalid next_page token {}".format(page_params['next_page']),
                    code=400
                )
                return manifest_info
            else:
                jobReference = jobDescription['jobReference']
                next_page = jobDescription['next_page']

            # If next_page is empty, then we timed out on the previous pass
            if not next_page:
                job_status = BigQuerySupport.wait_for_done(query_job={'jobReference': jobReference})

                # Decide how to proceed depending on job status (DONE, RUNNING, ERRORS)
                manifest_info = is_job_done(job_status, manifest_info, jobReference, user, 'manifest')
                if "message" in manifest_info:
                    return manifest_info
            manifest_info = {}
        else:
            manifest_info = dict(
                message="Invalid next_page token {}".format(page_params['next_page']),
                code=400
            )
            return manifest_info

        # manifest_info = validate_parameters(request, manifest_info, local_params, local_booleans, local_integers, None)
        #
        manifest_info, next_page = get_manifest_job_results(manifest_info,
                                                            page_params['page_size'],
                                                            jobReference,
                                                            next_page)

        logger.debug("get_manifest, manifest_info %s", manifest_info)

        if next_page:
            cipher_pageToken = encrypt_pageToken(user, jobReference,
                                                 next_page, 'manifest')
        else:
            cipher_pageToken = ""
        manifest_info['next_page'] = cipher_pageToken
    except Exception as e:
        logger.exception(e)
        manifest_info = dict(
            message='[ERROR] get_manifest(): Error trying to preview a cohort',
            code=400)

    return manifest_info


def is_job_done(job_is_done, manifest_info, jobReference, user, op):
    if job_is_done and job_is_done['status']['state'] == 'DONE':
        if 'status' in job_is_done and 'errors' in job_is_done['status']:
            job_id = job_is_done['jobReference']['jobId']
            logger.error("[ERROR] During query job {}: {}".format(job_id, str(
                job_is_done['status']['errors'])))
            logger.error("[ERROR] Error'd out query: {}".format(manifest_info['query']['sql_string']))
            return dict(
                message="[ERROR] During query job {}: {}".format(job_id, str(
                    job_is_done['status']['errors'])),
                code=500)
        else:
            # Don't return the query in this form

            manifest_info.pop('query', None)
    else:
        # We timed out waiting for the BQ job to complete.
        # Return the job ref so that the user can get the results when the job completes.

        # Don't return the query in this form
        manifest_info.pop('query', None)

        logger.error("[ERROR] API query took longer than the allowed time to execute. " +
                     "Retry the query using the next_page token.")
        cipher_pageToken = encrypt_pageToken(user, jobReference, "", op)
        # manifest_info['next_page'] = cipher_pageToken
        # manifest_info["cohortObjects"] = {
        #     "totalFound": 0,
        #     "rowsReturned": 0,
        #     "collections": [],
        # }
        manifest_info =  dict(
            next_page = cipher_pageToken,
            message="[ERROR] API query took longer than the allowed time to execute. " +
                    "Retry the query using the next_page token.",
            # manifest_info=manifest_info,
            code=202)
        return manifest_info

    return manifest_info


# Check if there are invalid keys
def validate_keys(request, manifest_info, params):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)

    for key in request.args.keys():
        match = blacklist.search(str(key))
        if match:
            manifest_info =  dict(
                message = "Key {} contains invalid characters; please edit and resubmit. " +
                           "[Saw {}]".format(str(key, match)),
                code = 400
            )

        if not key.lower() in params:
            manifest_info = dict(
                message="Invalid key {}".format(key),
                code=400
            )
    return manifest_info

def validate_parameters(request, manifest_info, params, booleans, integers, user):

    if user:
        params["email"] = user

    for key in params:
        if key in request.args:
            params[key] = request.args.get(key)

    for param in booleans:
        params[param] = params[param] in [True, 'True']

    try:
        for param in integers:
            params[param] = int(params[param])
    except ValueError:
        manifest_info = dict(
            message = "Parameter {} must have an integer value".format(param),
            code = 400
        )

    return manifest_info

# Get a list of GCS URLs or CRDC GUIDs of the instances in the cohort
def get_manifest_job_results(manifest_info, maxResults, jobReference, next_page):

    # field_name_map = dict(
    #     collection_id = 'collection_id',
    #     PatientID = 'PatientID',
    #     StudyInstanceUID = 'StudyInstanceUID',
    #     StopIteration = 'SeriesInstanceUID',
    #     SOPInstanceUID = 'SOPInstanceUID',
    #     source_DOI = 'source_DOI',
    #     crdc_study_uuid = 'crdc_study_uuid',
    #     crdc_series_uuid = 'crdc_series_uuid',
    #     crdc_instance_uuid = 'crdc_instance_uuid',
    #     gcs_bucket = 'gcs_bucket',
    #     gcs_url = 'gcs_url',
    #     aws_bucket = 'aws_bucket',
    #     aws_url = 'aws_url'
    # )

    field_name_map = {field_name: field_name for field_name in default_manifest_params}

    results = BigQuerySupport.get_job_result_page(job_ref=jobReference,
                                                  page_token=next_page,
                                                  maxResults=maxResults)

    schema_names = [field['name'] if field['name'] not in field_name_map.keys() else field_name_map[field['name']] for field in results['schema']['fields']]
    manifest_info["manifest"] = dict(
                totalFound = int(results['totalFound']),
                rowsReturned = len(results["current_page_rows"])
    )
    rows = form_rows_json(results['current_page_rows'], schema_names)
    manifest_info["manifest"]['json_manifest'] = rows

    # rowsReturned = len(results["current_page_rows"])
    return manifest_info, results['next_page']


def form_rows_json(data, schema_names):
    rows = []
    for row in data:
        row_vals = [ val['v'] for val in row['f']]
        row_dict = dict(zip(schema_names,row_vals))
        # for key in row_dict.keys():
        #     if 'GUID' in key:
        #         row_dict[key] = f"{CRDC_GUID_PREFIX}/{row_dict[key]}"
        rows.append(row_dict)

    return rows


