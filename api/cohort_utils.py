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
import copy
import json

from django.conf import settings
# from idc_collections.models import ImagingDataCommonsVersion
# from idc_collections.collex_metadata_utils import get_bq_metadata, get_bq_string
from google_helpers.bigquery.bq_support import BigQuerySupport


logger = logging.getLogger('main_logger')
BLACKLIST_RE = settings.BLACKLIST_RE

def submit_BQ_job(sql_string, params):
    results = BigQuerySupport.execute_query_and_fetch_results(sql_string, params, no_results=True)
    return results

def build_collections(objects, dois, urls):
    collections = []
    for collection in objects:
        patients = build_patients(collection, objects[collection], dois, urls)
        collections.append(
            {
                "collection_id":collection,
            }
        )
        if len(patients) > 0:
            collections[-1]["patients"] = patients
    return collections


def build_patients(collection,collection_patients, dois, urls):
    patients = []
    for patient in collection_patients:
        studies = build_studies(collection, patient, collection_patients[patient], dois, urls)
        patients.append({
                "patient_id":patient,
            }
        )
        if len(studies) > 0:
            patients[-1]["studies"] = studies
    return patients


def build_studies(collection, patient, patient_studies, dois, urls):
    studies = []
    for study in patient_studies:
        series = build_series(collection, patient, study, patient_studies[study], dois, urls)
        studies.append(
            {
                "StudyInstanceUID": study
            })
        if dois:
            studies[-1]["GUID"] = ""
        if urls:
            studies[-1]["AccessMethods"] = [
                    {
                        "access_url": "gs://gcs-public-data--healthcare-tcia-{}/dicom/{}".format(collection,study),
                        "region": "Multi-region",
                        "type": "gs"
                    }
            ]
        if len(series) > 0:
            studies[-1]["series"] = series
    return studies


def build_series(collection, patient, study, patient_studies, dois, urls):
    series = []
    for aseries in patient_studies:
        instances = build_instances(collection, patient, study, aseries, patient_studies[aseries], dois, urls)
        series.append(
            {
                "SeriesInstanceUID": aseries
            })
        if dois:
            series[-1]["GUID"] = ""
        if urls:
            series[-1]["AccessMethods"] = [
                {
                    "access_url": "gs://gcs-public-data--healthcare-tcia-{}/dicom/{}/{}".format(collection,
                                    study, aseries),
                    "region": "Multi-region",
                    "type": "gs"
                }
            ]
        if len(instances) > 0:
            series[-1]["instances"] = instances
    return series


def build_instances(collection, patient, study, series, study_series, dois, urls):
    instances = []
    for instance in study_series:
        instances.append(
            {
                "SOPInstanceUID": instance
            })
        if dois:
            instances[-1]["GUID"] = ""
        if urls:
            instances[-1]["AccessMethods"] = [
                {
                    "access_url": "gs://gcs-public-data--healthcare-tcia-{}/dicom/{}/{}/{}.dcm".format(collection,
                                    study,series,instance),
                    "region": "Multi-region",
                    "type": "gs"
                }
            ]
    return instances


def build_hierarchy(objects, rows, return_level, reorder):
#
    for raw in rows:
        rawv = [val['v'] for val in raw['f']]
        row = [rawv[i] for i in reorder]
        row[0] = row[0].replace('_','-')
        if not row[0] in objects:
            objects[row[0]] = {}
        if return_level == 'Collection':
            continue
        if not row[1] in objects[row[0]]:
            objects[row[0]][row[1]] = {}
        if return_level == 'Patient':
            continue
        if not row[2] in objects[row[0]][row[1]]:
            objects[row[0]][row[1]][row[2]] = {}
        if return_level == 'Study':
            continue
        if not row[3] in objects[row[0]][row[1]][row[2]]:
            objects[row[0]][row[1]][row[2]][row[3]] = []
        if return_level == 'Series':
            continue
        if not row[4] in objects[row[0]][row[1]][row[2]][row[3]]:
            # objects[row[0]][row[1]][row[2]][row[3]][row[4]] = {}
            objects[row[0]][row[1]][row[2]][row[3]].append(row[4])
    return objects

def form_rows(data):
    rows = []
    for row in data:
        if  row['f'][0]['v'] != None:
           rows.append(row['f'][0]['v'])
    return rows

def get_objects(return_level, cohort_info, maxResults):

    levels = {'Instance': ['collection_id', 'PatientID', 'StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID'],
              'Series': ['collection_id', 'PatientID', 'StudyInstanceUID', 'SeriesInstanceUID'],
              'Study': ['collection_id', 'PatientID', 'StudyInstanceUID'],
              'Patient': ['collection_id', 'PatientID'],
              'Collection': ['collection_id'],
              'None': []
              }

    return_level = return_level
    select = levels[return_level]

    objects = {}

    if return_level:
        results = BigQuerySupport.get_job_result_page(job_ref=cohort_info['job_reference'], page_token=cohort_info['next_page'], maxResults=maxResults)
        rowsReturned = len(results["current_page_rows"])

        # Create a list of the fields in the returned schema
        fields = [field['name'] for field in results['schema']['fields']]
        # Build a list of indices into fields that tells build_hierarchy how to reorder
        reorder = [fields.index(x) for x in select]

        # rows holds the actual data
        rows = results['current_page_rows']

        # We first build a tree of just the object IDS: collection_ids, PatientIDs, StudyInstanceUID,...
        objects = build_hierarchy(
            objects=objects,
            rows=rows,
            reorder=reorder,
            return_level=return_level)

        # Then we add the details such as DOI, URL, etc. about each object
        # dois = request.GET['return_DOIs'] in ['True', True]
        # urls = request.GET['return_URLs'] in ['True', True]
        dois = False
        urls = False
        collections = build_collections(objects, dois, urls)

        cohort_info["cohortObjects"] = {
            "totalFound": int(results['totalFound']),
            "rowsReturned": rowsReturned,
            "collections": collections,
        }
        cohort_info['next_page'] = results['next_page']

    return cohort_info


# Get a list of GCS URLs or CRDC DOIs of the instances in the cohort
def get_manifest(manifest_info, maxResults):

    results = BigQuerySupport.get_job_result_page(job_ref=manifest_info['job_reference'],
                                                  page_token=manifest_info['next_page'], maxResults=maxResults)
    # rows holds the actual data
    rows = form_rows(results['current_page_rows'])
    rowsReturned = len(results["current_page_rows"])

    access_method = 'doi' if results['schema']['fields'][0]['name'] =='crdc_instance_uuid' else 'url'

    manifest_info["manifest"] = dict(
                totalFound = int(results['totalFound']),
                rowsReturned = rowsReturned,
                url_access_type = "gs",
                url_region = "us",
                urls = rows if access_method == 'url' else [],
                dois = rows if access_method != 'url' else [],
    )
    manifest_info['next_page'] = results['next_page']


    return manifest_info


