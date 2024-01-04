# 
# Copyright 2019, Institute for Systems Biology
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
import requests
from .auth import get_auth

from flask import request
from werkzeug.exceptions import BadRequest

from python_settings import settings
from .manifest_utils import validate_body, validate_cohort_def, process_special_fields, encrypt_pageToken, decrypt_pageToken
from jsonschema import validate as schema_validate, ValidationError
from .version_config import API_VERSION
from google_helpers.bigquery.bq_support import BigQuerySupport
BLACKLIST_RE = settings.BLACKLIST_RE

logger = logging.getLogger(settings.LOGGER_NAME)

def convert_to_bool(s):
    if s in ['True']:
        s = True
    elif s in ['False']:
        s = False
    return s


def get_params(param_defaults):
    params = {}
    for key in param_defaults:
        params[key] = request.args.get(key)
        if params[key] == None:
            params[key] = param_defaults[key]
    return params


def post_query(body, user, cohort_id):
    try:
        body = validate_body(body)
        if 'message' in body:
            return body
        special_fields = body.pop('special_fields')

        query_info = perform_query(
                             f"{settings.BASE_URL}/cohorts/api/{API_VERSION}/{cohort_id}/query/",
                             body,
                             special_fields,
                             user=user)
        if "message" in query_info:
            return query_info
        query_info['cohort_def']['user_email'] = user['email']

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        query_info = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)

    return query_info


def post_query_preview(body, user=None):
    try:
        if not "cohort_def" in body:
            param_info = dict(
                message=f"'cohort_def' is required in the body",
                code=400
            )
            return param_info
        cohort_def = validate_cohort_def(body["cohort_def"])
        if 'message' in cohort_def:
            return cohort_def
        else:
            body['cohort_def'] = cohort_def

        body = validate_body(body)
        # request_data['cohort_def'], cohort_info = validate_cohort_definition(request_data['cohort_def'])
        if 'message' in body:
            return body
        special_fields = body.pop('special_fields')
        query_info = perform_query(
                             f"{settings.BASE_URL}/cohorts/api/{API_VERSION}/preview/query/",
                             body,
                             special_fields,
                             user=user)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        query_info = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)

    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        query_info = dict(
            message= e.message,
            code = 400)

    return query_info


def get_query_next_page(user):
    query_info = query_next_page(request, user)
    return query_info


def generate_user_sql_string(query_info):
    sql = query_info['query']['sql_string']
    for param_list in query_info['query']['params']:
        for param in param_list:
            if param['parameterType']['type'] == 'STRING':
                sql = sql.replace(f"@{param['name']}", f'"{param["parameterValue"]["value"]}"')
            elif param['parameterType']['type'] == 'NUMERIC':
                sql = sql.replace(f"@{param['name']}", str(param["parameterValue"]["value"]))
            elif param['parameterType']['type'] == 'ARRAY' and param['parameterType']['arrayType']['type'] == 'STRING':
                sql = sql.replace(f"@{param['name']}",json.dumps([value['value'] for value in param['parameterValue']['arrayValues']]))
            else:
                logger.warning("[WARNING] Unsupported SQL type")
                query_info = dict(
                    message='Internal server error. Please report.',
                    code=400)
    query_info['cohort_def']['sql'] = sql
    return query_info


def perform_query(url, body, special_fields, user):  # , user=None):
    next_page = ""
    try:
        data = {
            "request_data": body,
            "email": user['email']
        }

        auth = get_auth()
        results = requests.post(url, json=data, headers=auth)
        query_info = results.json()
        if "message" in query_info:
            return query_info

        if data['request_data']['sql']:
            generate_user_sql_string(query_info)
        query_info = process_special_fields(special_fields, query_info, data)

        # Start the BQ job, but don't get any data results, just the job info.
        job_status = submit_BQ_job(query_info['query']['sql_string'],
                                    query_info['query']['params'])
        jobReference = job_status['jobReference']

        # Decide how to proceed depending on job status (DONE, RUNNING, ERRORS)
        query_info = is_job_done(job_status, query_info, jobReference, user)
        if "message" in query_info:
            return query_info
        query_info, next_page = get_query_job_results(query_info, body['page_size'],
                                    jobReference, next_page)
        if next_page:
            cipher_pageToken = encrypt_pageToken(user, jobReference, next_page, 'query')
        else:
            cipher_pageToken = ""
        query_info['next_page'] = cipher_pageToken


    except Exception as e:
        logger.exception(e)
        query_info = dict(
            message='[ERROR] get_query(): Error trying to get a manifest',
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
            # jobDescription = decrypt_pageToken(user, request.args.get('next_page'), 'query')
            jobDescription = decrypt_pageToken(user, page_params['next_page'], 'query')
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
            query_info = dict()
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


def submit_BQ_job(sql_string, params):
    results = BigQuerySupport.execute_query_and_fetch_results(sql_string, params, no_results=True)
    return results

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


def get_query_job_results(query_info, maxResults, jobReference, next_page):

    results = BigQuerySupport.get_job_result_page(job_ref=jobReference,
                                                  page_token=next_page,
                                                  maxResults=maxResults)

    schema_names = [field['name'] for field in results['schema']['fields']]

    query_info["manifest"] = dict(
                totalFound = int(results['totalFound']),
                rowsReturned = len(results["current_page_rows"])
    )
    rows = form_rows_json(results['current_page_rows'], schema_names, results['schema']['fields'])
    query_info["manifest"]['manifest_data'] = rows

    return query_info, results['next_page']


def form_rows_json(data, schema_names, schema):
    rows = []
    integer_fields = [field['name'] for field in schema if field['type'] == 'INTEGER']
    for row in data:
        # row_vals = [ val['v'] for val in row['f']]
        row_vals = [unpack(val) for val in row['f']]
        new_row = dict(zip(schema_names,row_vals))
        for field in integer_fields:
            new_row[field] = int(new_row[field]) if not new_row[field] is None else None
        rows.append(new_row)

    return rows

def unpack(val):
    if not type(val['v']) == list:
        return val['v']
    else:
        return [subval['v'] for subval in val['v']]




