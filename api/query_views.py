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
import re
import json
import requests

from flask import request
from werkzeug.exceptions import BadRequest

from python_settings import settings
from . query_utils import perform_query, perform_fixed_query
from jsonschema import validate as schema_validate, ValidationError
from . schemas.filterset import COHORT_FILTER_SCHEMA

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

def _query_metadata():

    sql_string =  """
    #standardSQL
    SELECT
        AdditionalPatientHistory,
        Allergies,
        BodyPartExamined,
        collection_id,
        crdc_instance_uuid,
        crdc_series_uuid,
        crdc_study_uuid,
        EthnicGroup,
        gcs_bucket,
        gcs_generation,
        gcs_url,
        ImageType,
        LastMenstrualDate,
        MedicalAlerts,
        Modality,
        Occupation,
        PatientAge,
        PatientComments,
        PatientID,
        PatientSize,
        PatientWeight,
        PregnancyStatus,
        ReasonForStudy,
        RequestedProcedureComments,
        SeriesInstanceUID,
        SmokingStatus,
        SOPClassUID,
        SOPInstanceUID,
        Source_DOI,
        StudyID,
        StudyInstanceUID,
        tcia_tumorLocation
    FROM `canceridc-data.idc_views.dicom_all`
    """

    try:
        query_info = perform_fixed_query(request, sql_string)

    except Exception as e:
        logger.exception(e)
        query_info = dict(
            message='[ERROR] _query(): Error performing corhorts/metadata/query',
            code=400)

    return query_info

    

def get_query_info(user, cohort_id):
    query_info = perform_query(request,
                                 func=requests.get,
                                 url="{}/cohorts/api/{}/".format(settings.BASE_URL, cohort_id),
                                 user=user)
    return query_info




def post_query_preview():
    try:
        request_data = request.get_json()

        if 'filterSet' not in request_data:
            return dict(
                message = 'No filters were provided; ensure that the request body contains a \'filterSet\' property.',
                code = 400)

        schema_validate(request_data['filterSet'], COHORT_FILTER_SCHEMA)

        if 'name' not in request_data:
            return dict(
                message = 'A name was not provided for this cohort. The cohort was not made.',
                code = 400
            )

        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match = blacklist.search(str(request_data['name']))

        if not match and 'description' in request_data:
            match = blacklist.search(str(request_data['description']))

        if match:
            return dict(
                message = "Your cohort's name or description contains invalid characters; " +
                            "please edit them and resubmit. [Saw {}]".format(str(match)),
                code = 400
            )

        data = {"request_data": request_data}

        query_info = get_query(request,
                             func=requests.post,
                             url="{}/cohorts/api/preview/".format(settings.BASE_URL),
                             data=data)

    except BadRequest as e:
        logger.warning("[WARNING] Received bad request - couldn't load JSON.")
        query_info = dict(
            message='The JSON provided in this request appears to be improperly formatted.',
            code = 400)

    except ValidationError as e:
        logger.warning('[WARNING] Filters rejected for improper formatting: {}'.format(e))
        query_info = dict(
            message= 'Filters were improperly formatted.',
            code = 400)

    return query_info








