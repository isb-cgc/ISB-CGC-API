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

from cryptography.fernet import Fernet, InvalidToken

import settings

from .schemas.queryfields import QUERY_FIELDS
from .schemas.filters import COHORT_FILTERS_SCHEMA
from jsonschema import validate as schema_validate, ValidationError

logger = logging.getLogger('main_logger')
BLACKLIST_RE = settings.BLACKLIST_RE

cipher_suite = Fernet(settings.PAGE_TOKEN_KEY)

default_query_params = {
    "counts": False,
    "group_size": False,
    "page_size": 1000,
    "sql": False
}

body_keys = ["fields", "counts", "group_size", "page_size", "sql"]
preview_body_keys = ["cohort_def", "fields", "counts", "group_size", "page_size", "sql"]
cohort_def_keys = ["name", "description", "filters"]

lowered_query_params = {key.lower(): key for key in default_query_params}


def encrypt_pageToken(user, jobReference, next_page, op):
    # cipher_suite = Fernet(settings.PAGE_TOKEN_KEY)
    jobDescription = dict(
        email = user['email'],
        remote_addr = user['remote_addr'],
        jobReference = jobReference,
        next_page = next_page,
        op = op
    )
    plain_jobDescription = json.dumps(jobDescription).encode()

    cipher_jobReference = cipher_suite.encrypt(plain_jobDescription).decode()

    return cipher_jobReference


def decrypt_pageToken(user, cipher_jobReference, op):
    try:
        plain_jobDescription = cipher_suite.decrypt(cipher_jobReference.encode())
        jobDescription = json.loads(plain_jobDescription.decode())
        if jobDescription["email"] != user['email']:
            # Caller's email doesn't match what was encrypted
            logger.error("Caller's email, {}, doesn't match what was encrypted: {}".format(
                user['email'], jobDescription['email']))
            return {}
        elif jobDescription["remote_addr"] != user['remote_addr']:
            # Caller's email doesn't match what was encrypted
            logger.error("Caller's remote_addr, {}, doesn't match what was encrypted: {}".format(
                user['remote_addr'], jobDescription['remote_addr']))
            return {}
        elif jobDescription["op"] != op:
            # Caller's email doesn't match what was encrypted
            logger.error("Incorrect next_page endpoint for next_page token".format(
                op, jobDescription['email']))
            return {}
        else:
            jobDescription.pop('email')
            jobDescription.pop('remote_addr')
            jobDescription.pop('op')
            return jobDescription
    except InvalidToken:
        logger.error("Could not decrypt token: {}".format(cipher_jobReference))
        return {}



def normalize_query_fields(fields):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    corrected_fields = []
    special_fields = []
    lowered_fields = {key.lower(): key for key in QUERY_FIELDS['properties']['fields']['items']['enum']}
    # lowered_fields = {key.lower(): key for key in QUERY_FIELDS['items']['enum']}
    for field in fields:
        match = blacklist.search(str(filter))
        if match:
            result = dict(
                message="Field '{}' contains invalid characters; please edit and resubmit. " +
                        "[Saw {}]".format(str(field, match)),
                code=400
            )

        if field.lower() in [
                'counts',
                'group_size',
                "patientage",
                "patientsex",
                "patientsize",
                "patientweight"]:
            special_fields.append(field.lower())
        elif field.lower() in lowered_fields:
            corrected_fields.append(lowered_fields[field.lower()])
            if field.lower() in ['studydate', 'studydescription']:
                special_fields.append(field.lower())
        else:
            return (corrected_fields, special_fields, dict(
                message=f'{field} is not a valid field.',
                code=400
            )
                    )
    return corrected_fields, special_fields, {}

def process_special_fields(special_fields, query_info, data):
    if special_fields:
        fields = set([field.lower() for field in data['request_data']['fields']])
        sql_string = query_info['query']['sql_string']
        # sql_string = 'SELECT'
        select_string = sql_string[0:sql_string.find('FROM')]
        if 'WHERE' in sql_string:
            from_string = sql_string[sql_string.find('FROM'):sql_string.find('WHERE')]
            where_string =sql_string[sql_string.find('WHERE'):sql_string.find('GROUP')]
        else:
            from_string = sql_string[sql_string.find('FROM'):sql_string.find('GROUP')]
            where_string = ""
        group_by_string = sql_string[sql_string.find('GROUP'):sql_string.find('ORDER')]
        order_by_string = sql_string[sql_string.find('ORDER'):]

        # Include counts if there is an explicit level
        if 'counts' in special_fields:
            if {'crdc_instance_uuid', 'sopinstanceuid'} & fields:
                pass

            elif {'crdc_series_uuid', 'seriesinstanceuid'} & fields:
                select_string = select_string.replace('SELECT', 'SELECT COUNT(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,')

            elif {'crdc_study_uuid', 'studyinstanceuid'} & fields:
                select_string = select_string.replace('SELECT', \
        '''SELECT COUNT(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,
        COUNT(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,''')

            elif {'patientid'} & fields:
                select_string = select_string.replace('SELECT', \
        '''SELECT COUNT(DISTINCT dicom_pivot.StudyInstanceUID) study_count,
        COUNT(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,
        COUNT(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,''')

            elif {'collection_id'} & fields:
                select_string = select_string.replace('SELECT', \
        '''SELECT COUNT(DISTINCT dicom_pivot.patientID) patient_count,
        COUNT(DISTINCT dicom_pivot.StudyInstanceUID) study_count,
        COUNT(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,
        COUNT(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,''')

            else:
                select_string = select_string.replace('SELECT', \
        '''SELECT COUNT(DISTINCT dicom_pivot.collection_id) collection_count, 
        COUNT(DISTINCT dicom_pivot.patientID) patient_count,
        COUNT(DISTINCT dicom_pivot.StudyInstanceUID) study_count,
        COUNT(DISTINCT dicom_pivot.SeriesInstanceUID) series_count,
        COUNT(DISTINCT dicom_pivot.SOPInstanceUID) instance_count,''')

        if 'group_size' in special_fields:
            select_string = select_string.replace('SELECT', 'SELECT sum(dicom_pivot.instance_size) group_size,')

        if 'studydate' in special_fields:
            # The study date is grouped
            # Replace the first instance of 'dicom_pivot.StudyDate' with an aggregation
            select_string = select_string.replace('dicom_pivot.StudyDate', 'MIN(dicom_pivot.StudyDate) StudyDate', 1)
            # Get the instance in the GROUP BY clause and delete it
            offset = group_by_string.find('dicom_pivot.StudyDate', group_by_string.find('GROUP BY'))
            group_by_string = group_by_string[:offset].rstrip(" ,") + ' ' + group_by_string[offset:].replace('dicom_pivot.StudyDate', '', 1)
            order_by_string = order_by_string.replace('dicom_pivot.StudyDate', 'StudyDate', 1)

        if 'studydescription' in special_fields:
            # The StudyDescription is grouped
            # Replace the first instance of 'dicom_pivot.StudyDate' with an aggregation
            select_string = select_string.replace('dicom_pivot.StudyDescription', \
                'STRING_AGG(DISTINCT dicom_pivot.StudyDescription, "," ORDER BY dicom_pivot.StudyDescription) StudyDescription', 1)
            # Get the instance in the GROUP BY clause and delete it
            offset = group_by_string.find('dicom_pivot.StudyDescription', group_by_string.find('GROUP BY'))
            group_by_string = group_by_string[:offset].rstrip(" ,") + ' ' + group_by_string[offset:].replace('dicom_pivot.StudyDescription', '', 1)
            offset = order_by_string.find('dicom_pivot.StudyDescription', order_by_string.find('ORDER BY', offset))
            order_by_string = order_by_string.replace('dicom_pivot.StudyDescription', 'StudyDescription', 1)

        for field in [
                "PatientAge",
                "PatientSex",
                "PatientSize",
                "PatientWeight"]:
            if field.lower() in special_fields:
                select_string = select_string.replace("SELECT", f"SELECT dicom_pivot.{field}, ")
                group_by_string = group_by_string.replace("GROUP BY", f"GROUP BY dicom_pivot.{field}, ")
                order_by_string= order_by_string.replace("ORDER BY", f"ORDER BY dicom_pivot.{field}, ")

        query_info['query']['sql_string'] = select_string + from_string + where_string + group_by_string + order_by_string
        if query_info['cohort_def']['sql']:
            query_info['cohort_def']['sql'] = \
                select_string + \
                query_info['cohort_def']['sql'][query_info['cohort_def']['sql'].find('FROM'):query_info['cohort_def']['sql'].find('GROUP BY')] + \
                group_by_string + order_by_string
                # query_info['cohort_def']['sql'].replace('SELECT', sql_string)
    return query_info


def validate_key(key):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    result = {}
    match = blacklist.search(str(key))
    if match:
        result =  dict(
            message = "Key '{}' contains invalid characters; please edit and resubmit. " +
                       "[Saw {}]".format(str(key, match)),
            code = 400
        )
    return result

# Deal with casing issues in filterset, converting to normalized values
def normalize_filterset(filterset):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    corrected_filters = {}
    lowered_filters = {key.lower(): key for key in COHORT_FILTERS_SCHEMA['properties'].keys()}
    for filter, value in filterset.items():
        match = blacklist.search(str(filter))
        if match:
            result = dict(
                message="Filter '{}' contains invalid characters; please edit and resubmit. " +
                        "[Saw {}]".format(str(filter, match)),
                code=400
            )
        match = blacklist.search(str(value))
        if match:
            result = dict(
                message="Value '{}' of filter '{}' contains invalid characters; please edit and resubmit. " +
                        "[Saw {}]".format(str(value, filter, match)),
                code=400
            )
        if filter.lower() in lowered_filters:
            corrected_filters[lowered_filters[filter.lower()]] = value
        else:
            return (filterset, dict(
                message=f'{filter} is not a valid filter.',
                code=400
            )
                    )
    return corrected_filters, {}


def validate_cohort_def(cohort_def):
    for key in cohort_def.keys():
        if not key in cohort_def_keys:
            param_info = dict(
                message=f"'{key}' is an invalid cohort_def key",
                code=400
            )
            return param_info

    if not 'filters' in cohort_def:
        param_info = dict(
            message=f"'filters' is a required cohort_def key",
            code=400
        )
        return param_info

    if not "name" in cohort_def:
        cohort_def["name"] = ""
    else:
        result = validate_key("name")
        if 'message' in result:
            return result

    if not "description" in cohort_def:
        cohort_def["description"] = ""
    else:
        result = validate_key("description")
        if 'message' in result:
            return result

    # Replace submitted filter IDs with normalized filter IDs
    cohort_def['filters'], filter_info = normalize_filterset(cohort_def['filters'])
    if 'message' in filter_info:
        return(cohort_def, filter_info)
    # Validate the filterset
    try:
        schema_validate(cohort_def['filters'], COHORT_FILTERS_SCHEMA)
    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        result = dict(
            message= 'Filters were improperly formatted.',
            code = 400)
        return result

    return cohort_def


# Validate the body of a /cohort/manifest request except for the cohort_def, which is validated separately
def validate_body(body):
    for key in body.keys() :
        if not key in preview_body_keys:
            param_info = dict(
                message=f"{key} is an invalid body key",
                code=400
            )
            return param_info

    if not "fields" in body:
        param_info = dict(
            message=f"fields is required in the body",
            code=400
        )
        return param_info

    for key in ['counts', 'group_size', 'sql']:
        if not key in body:
            body[key] = False
        else:
            body[key] = bool(body[key])

    if not 'page_size' in body:
        body['page_size'] = 1000
    elif not isinstance(body['page_size'], int):
        error_info = dict(
            message=f"page_size value must be an integer",
            code=400
        )
        return error_info

    body['fields'], special_fields, error_info = normalize_query_fields(body['fields'])
    if body['counts']:
        special_fields.append('counts')
    if body['group_size']:
        special_fields.append('group_size')
    if error_info:
        return error_info
    body['special_fields'] = special_fields

    if not body['fields']:
        manifest_info = dict(
            message=f'At least one query parameter must be True.',
            code=400
        )

    return body




