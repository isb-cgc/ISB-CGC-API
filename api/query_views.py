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
from . schemas.querypreviewbody import QUERY_PREVIEW_BODY
from . schemas.queryfields import QUERY_FIELDS

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

def get_query_metadata():

    sql_string =  """
    #standardSQL
    SELECT
        PatientID,
        BodyPartExamined,
        SeriesInstanceUID,
        SliceThickness,
        SeriesNumber,
        SeriesDescription,
        StudyInstanceUID,
        StudyDescription,
        StudyDate,
        SOPInstanceUID,
        Modality,
        SOPClassUID,
        crdc_study_uuid,
        crdc_series_uuid,
        crdc_instance_uuid,
        Program,
        tcia_tumorLocation,
        source_DOI,
        tcia_species,
        collection_id,
        Internal_structure,
        Sphericity,
        Calcification,
        Lobular_Pattern,
        Spiculation,
        Margin,
        Texture,
        Subtlety_score,
        Malignancy,
        SUVbw,
        Volume,
        Diameter,
        Surface_area_of_mesh,
        Total_Lesion_Glycolysis,
        Standardized_Added_Metabolic_Activity,
        Apparent_Diffusion_Coefficient,
        Percent_Within_First_Quarter_of_Intensity_Range,
        Percent_Within_Third_Quarter_of_Intensity_Range,
        Percent_Within_Fourth_Quarter_of_Intensity_Range,
        Percent_Within_Second_Quarter_of_Intensity_Range,
        Standardized_Added_Metabolic_Activity_Background,
        Glycolysis_Within_First_Quarter_of_Intensity_Range,
        Glycolysis_Within_Third_Quarter_of_Intensity_Range,
        Glycolysis_Within_Fourth_Quarter_of_Intensity_Range,
        Glycolysis_Within_Second_Quarter_of_Intensity_Range,
        AnatomicRegionSequence,
        SegmentedPropertyCategoryCodeSequence,
        SegmentedPropertyTypeCodeSequence,
        FrameOfReferenceUID,
        SegmentNumber,
        SegmentAlgorithmType

    FROM `canceridc-data.idc_v2.dicom_pivot_v2`
    ORDER BY collection_id, PatientID, StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID
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




def post_query(user, cohort_id):
    try:
        request_data = request.get_json()

        if 'fields' not in request_data:
            return dict(
                message = 'No queryFields provided; ensure that the request body contains a \'queryFields\' component.',
                code = 400)

        schema_validate(request_data, QUERY_FIELDS)

        data = {"request_data": request_data}

        query_info = perform_query(request,
                             func=requests.post,
                             url="{}/cohorts/api/{}/query/".format(settings.BASE_URL,cohort_id),
                             data=data,
                             user=user)

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


def post_query_preview():
    try:
        request_data = request.get_json()

        if 'cohort_def' not in request_data:
            return dict(
                message = 'No cohort_def provided; ensure that the request body contains a \'cohort_dev\' component.',
                code = 400)
        if 'filters' not in request_data['cohort_def']:
            return dict(
                message = 'No filters were provided; ensure that the cohort_def contains a \'filterSet\' component.',
                code = 400)
        if 'queryFields' not in request_data:
            return dict(
                message = 'No queryFields provided; ensure that the request body contains a \'queryFields\' component.',
                code = 400)

        schema_validate(request_data, QUERY_PREVIEW_BODY)

        if 'name' not in request_data["cohort_def"] or request_data["cohort_def"]['name'] == "":
            return dict(
                message = 'A name was not provided for this cohort. The cohort was not made.',
                code = 400
            )

        blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
        match = blacklist.search(str(request_data["cohort_def"]['name']))

        if not match and 'description' in request_data["cohort_def"]:
            match = blacklist.search(str(request_data["cohort_def"]['description']))

        if match:
            return dict(
                message = "Your cohort's name or description contains invalid characters; " +
                            "please edit them and resubmit. [Saw {}]".format(str(match)),
                code = 400
            )

        data = {"request_data": request_data}

        query_info = perform_query(request,
                             func=requests.post,
                             url="{}/cohorts/api/preview/query/".format(settings.BASE_URL),
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








