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

from .auth import get_auth
from cryptography.fernet import Fernet, InvalidToken

import settings
from google_helpers.bigquery.bq_support import BigQuerySupport
from .cohort_utils import encrypt_pageToken, decrypt_pageToken, validate_query_parameters,\
    default_query_params, lowered_query_params
from .schemas.queryfields import QUERY_FIELDS

logger = logging.getLogger('main_logger')
BLACKLIST_RE = settings.BLACKLIST_RE

cipher_suite = Fernet(settings.PAGE_TOKEN_KEY)


def submit_BQ_job(sql_string, params):
    results = BigQuerySupport.execute_query_and_fetch_results(sql_string, params, no_results=True)
    return results


def normalize_query_fields(fields):
    corrected_fields = []
    special_fields = []
    lowered_fields = {key.lower(): key for key in QUERY_FIELDS['properties']['fields']['items']['enum']}
    # lowered_fields = {key.lower(): key for key in QUERY_FIELDS['items']['enum']}
    for field in fields:
        if field.lower() in ['counts', 'sizes']:
            special_fields.append(field.lower())
        elif field.lower() in lowered_fields:
            corrected_fields.append(lowered_fields[field.lower()])
        else:
            return (corrected_fields, special_fields, dict(
                message=f'{field} is not a valid field.',
                code=400
            )
                    )
    return corrected_fields, special_fields, {}

def add_counts_and_sizes(special_fields, query_info, data):
    if special_fields:
        fields = set([field.lower() for field in data['request_data']['fields']])
        sql_string = query_info['query']['sql_string']
        # Include counts if there is an explicit level
        if 'counts' in special_fields:
            if {'crdc_instance_uuid', 'sopinstanceuid'} & fields:
                pass
            elif {'crdc_sseries_uuid', 'seriesinstanceuid'} & fields:
                sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,')
            elif {'crdc_study_uuid', 'studyinstanceuid'} & fields:
                sql_string = sql_string.replace('SELECT', \
        '''SELECT count(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,
        count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,''')
            elif {'patientid'} & fields:
                sql_string = sql_string.replace('SELECT', \
        '''SELECT count(DISTINCT dicom_pivot.StudyInstanceUID) study_count,
        count(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,
        count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,''')
            elif {'collection_id'} & fields:
                sql_string = sql_string.replace('SELECT', \
        '''SELECT count(DISTINCT dicom_pivot.patientID) patient_count,
        count(DISTINCT dicom_pivot.StudyInstanceUID) study_count,
        count(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,
        count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,''')
            else:
                sql_string = sql_string.replace('SELECT', \
        '''SELECT count(DISTINCT dicom_pivot.collection_id) collection_count, 
        count(DISTINCT dicom_pivot.patientID) patient_count,'
        count(DISTINCT dicom_pivot.StudyInstanceUID) study_count,
        count(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,
        count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,''')
            # if 'sopinstanceuid' in fields:
            #     pass
            # elif 'seriesinstanceuid' in fields:
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,')
            # elif 'studyinstanceuid' in fields:
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,')
            # elif 'patientid' in fields:
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.StudyInstanceUID) study_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,')
            # elif 'collection_id' in fields:
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.patientID) patient_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.StudyInstanceUID) study_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,')
            # else:
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.collection_id) collection_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.patientID) patient_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.StudyInstanceUID) study_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,')
            #     sql_string = sql_string.replace('SELECT', 'SELECT count(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,')
        if 'sizes' in special_fields:
            if 'sopinstanceuid' in fields:
                sql_string = sql_string.replace('SELECT', 'SELECT ROUND(sum(dicom_pivot.instance_size)/POW(10,6), 2) instance_size_MB,')
            elif 'seriesinstanceuid' in fields:
                sql_string = sql_string.replace('SELECT', 'SELECT ROUND(sum(dicom_pivot.instance_size)/POW(10,6), 2) series_size_MB,')
            elif 'studyinstanceuid' in fields:
                sql_string = sql_string.replace('SELECT', 'SELECT ROUND(sum(dicom_pivot.instance_size)/POW(10,6), 2) study_size_MB,')
            elif 'patientid'  in fields:
                sql_string = sql_string.replace('SELECT', 'SELECT ROUND(sum(dicom_pivot.instance_size)/POW(10,6), 2) patient_size_MB,')
            elif 'collection_id' in fields:
                sql_string = sql_string.replace('SELECT', 'SELECT ROUND(sum(dicom_pivot.instance_size)/POW(10,6), 2) collection_size_MB,')


        query_info['query']['sql_string'] = sql_string
    return query_info



def perform_query(request, func, url, data=None, user=None): #, user=None):
    next_page = ""
    try:
        query_params = request.get_json()

        query_params, error_info = validate_query_parameters(request, \
                default_query_params.copy(), lowered_query_params)
        if error_info:
            return error_info

        data['request_data']['fields'], special_fields, error_info = normalize_query_fields(data['request_data']['fields'])
        if error_info:
            return error_info

        # if user:
        #     query_params['email'] = user
        auth = get_auth()
        if func == requests.post:
            results = func(url, params=query_params, json=data, headers=auth)
        else:
            results = func(url, params=query_params, headers=auth)
        query_info = results.json()
        if "message" in query_info:
            return query_info

        query_info = add_counts_and_sizes(special_fields, query_info, data)

        # Start the BQ job, but don't get any data results, just the job info.
        job_status = submit_BQ_job(query_info['query']['sql_string'],
                                    query_info['query']['params'])
        jobReference = job_status['jobReference']

        # Decide how to proceed depending on job status (DONE, RUNNING, ERRORS)
        query_info = is_job_done(job_status, query_info, jobReference, user)
        if "message" in query_info:
            return query_info
        query_info, next_page = get_query_job_results(query_info, query_params['page_size'],
                                    jobReference, next_page)
        if next_page:
            cipher_pageToken = encrypt_pageToken(user, jobReference, next_page, 'query')
        else:
            cipher_pageToken = ""
        query_info['next_page'] = cipher_pageToken

    except Exception as e:
        logger.exception(e)
        query_info = dict(
            message='[ERROR] get_query(): Error trying to preview a cohort',
            code=400)

    return query_info


def query_next_page(request, user):
    query_info = {}
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
        # if 'next_page' in request.args and \
        #     not request.args.get('next_page') in ["", None]:
        if not page_params['next_page'] in ["", None]:
            # We have a non-empty next_page token
            jobDescription = decrypt_pageToken(user, request.args.get('next_page'), 'query')
            if jobDescription == {}:
                query_info = dict(
                    message="Invalid next_page token {}".format(request.args.get('next_page')),
                    code=400
                )
                return query_info
            else:
                jobReference = jobDescription['jobReference']
                next_page = jobDescription['next_page']

            # If next_page is empty, then we timed out on the previous pass
            if not next_page:
                job_status = BigQuerySupport.wait_for_done(query_job={'jobReference':jobReference})

                # Decide how to proceed depending on job status (DONE, RUNNING, ERRORS)
                query_info = is_job_done(job_status, query_info, jobReference, user)
                if "message" in query_info:
                    return query_info
            query_info = dict(
                cohort = {},
            )
        else:
            query_info = dict(
                message="Invalid next_page token {}".format(request.args.get('next_page')),
                code=400
            )
            return query_info

        if "message" in query_info:
            return query_info

        query_info, next_page = get_query_job_results(query_info,
                                                            page_params['page_size'],
                                                            jobReference,
                                                            next_page)
        if next_page:
            cipher_pageToken = encrypt_pageToken(user, jobReference, next_page, 'query')
        else:
            cipher_pageToken = ""
        query_info['next_page'] = cipher_pageToken

    except Exception as e:
        logger.exception(e)
        query_info = dict(
            message='[ERROR] get_query(): Error trying to preview a cohort',
            code=400)

    return query_info


def is_job_done(job_is_done, query_info, jobReference, user):
    if job_is_done and job_is_done['status']['state'] == 'DONE':
        if 'status' in job_is_done and 'errors' in job_is_done['status']:
            job_id = job_is_done['jobReference']['jobId']
            logger.error("[ERROR] During query job {}: {}".format(job_id, str(
                job_is_done['status']['errors'])))
            logger.error("[ERROR] Error'd out query: {}".format(query_info['query']['sql_string']))
            return dict(
                message="[ERROR] During query job {}: {}".format(job_id, str(
                    job_is_done['status']['errors'])),
                code=500)
        else:
            # Don't return the query in this form

            query_info.pop('query', None)
    else:
        # We timed out waiting for the BQ job to complete.
        # Return the job ref so that the user can get the results when the job completes.

        # Don't return the query in this form
        query_info.pop('query', None)

        logger.error("[ERROR] API query took longer than the allowed time to execute. " +
                     "Retry the query using the next_page token.")
        cipher_pageToken = encrypt_pageToken(user, jobReference, "", 'query')
        query_info['next_page'] = cipher_pageToken
        query_info["cohortObjects"] = {
            "totalFound": 0,
            "rowsReturned": 0,
            "collections": [],
        }
        return dict(
            message="[ERROR] API query took longer than the allowed time to execute. " +
                    "Retry the query using the next_page token.",
            query_info=query_info,
            code=202)

    return query_info


# Check if there are invalid keys
def validate_keys(request, query_info, params):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)

    for key in request.args.keys():
        match = blacklist.search(str(key))
        if match:
            query_info =  dict(
                message = "Key {} contains invalid characters; please edit and resubmit. " +
                           "[Saw {}]".format(str(key, match)),
                code = 400
            )
        if not key in params:
            query_info = dict(
                message="Invalid key {}".format(key),
                code=400
            )
    return query_info

def validate_parameters(request, query_info, params, booleans, integers, user):

    try:
        for param in integers:
            params[param] = int(params[param])
    except ValueError:
        query_info = dict(
            message = "Parameter {} must have an integer value".format(param),
            code = 400
        )

    if user:
        params["email"] = user

    for key in params:
        if key in request.args:
            params[key] = request.args.get(key)

    for param in booleans:
        params[param] = params[param] in [True, 'True']

    return query_info

def get_query_job_results(query_info, maxResults, jobReference, next_page):

    results = BigQuerySupport.get_job_result_page(job_ref=jobReference,
                                                  page_token=next_page,
                                                  maxResults=maxResults)

    schema_names = [field['name'] for field in results['schema']['fields']]

    query_info["query_results"] = dict(
                totalFound = int(results['totalFound']),
                rowsReturned = len(results["current_page_rows"])
    )
    rows = form_rows_json(results['current_page_rows'], schema_names)
    query_info["query_results"]['json'] = rows

    # rowsReturned = len(results["current_page_rows"])
    return query_info, results['next_page']


def form_rows_json(data, schema_names):
    rows = []
    for row in data:
        # row_vals = [ val['v'] for val in row['f']]
        row_vals = [unpack(val) for val in row['f']]
        rows.append(dict(zip(schema_names,row_vals)))

    return rows

def unpack(val):
    if not type(val['v']) == list:
        return val['v']
    else:
        return [subval['v'] for subval in val['v']]




