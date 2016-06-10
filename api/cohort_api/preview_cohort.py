"""

Copyright 2015, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import endpoints
import logging
import MySQLdb

from protorpc import remote, messages
from django.core.signals import request_finished

import cohort_helpers
from api.api_helpers import sql_connection

logger = logging.getLogger(__name__)


class CohortPatientsSamplesList(messages.Message):
    patients = messages.StringField(1, repeated=True)
    patient_count = messages.IntegerField(2)
    samples = messages.StringField(3, repeated=True)
    sample_count = messages.IntegerField(4)
    cohort_id = messages.IntegerField(5)

# for v1, looks like this:
# service = discovery.build('cohort_api', 'v1', discoveryServiceURL='', http=httplib2.Http())
# data = service.cohort_endpoints().cohorts().preview_cohort( body = payload).execute

# 'cohort_api' comes from name in the endpoints.api class
# Cohort_Endpoints = endpoints.api(name='cohort_api', version='v1',
#                                  description="Get information about cohorts, patients, and samples. Create and delete cohorts.",
#                                  allowed_client_ids=[INSTALLED_APP_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])

# 'cohort_endpoints' comes from resource_name in the @Cohort_Endpoints.api_class decorator
# change this to 'cohorts', 'participants'
# @Cohort_Endpoints.api_class(resource_name='cohort_endpoints')

# 'cohorts().preview_cohort' comes from name='cohorts.preview_cohort' in @endpoints.method decorator
#     @endpoints.method(POST_RESOURCE, CohortPatientsSamplesList,
#                       path='preview_cohort', http_method='POST', name='cohorts.preview_cohort')

# changes for v2
# in isb_cgc_api/isb_cgc_api_helpers.py:
# ISB_CGC_Endpoints = endpoints.api(name='isb_cgc_api', version='v2', description=..., allowed_client_ids=...)

# in isb_cgc_api/cohort_resource.py:
# @isb_cgc_api_helpers.ISB_CGC_Endpoints.api_class(resource_name='cohorts')
# class CohortAPI(remote.Service):
#   POST_RESOURCE = ...
#   @endpoints.method(POST_RESOURCE, CohortPatientSamplesList, path='preview', name='preview')  # is name='preview' necessary?
#       def preview(self, request):
#           ...

@cohort_helpers.Cohort_Endpoints2.api_class(resource_name='preview_cohort_endpoints')
class PreviewCohort(remote.Service):
    POST_RESOURCE = endpoints.ResourceContainer(cohort_helpers.MetadataRangesItem)

    @endpoints.method(POST_RESOURCE, CohortPatientsSamplesList,
                      path='preview_cohort2', http_method='POST', name='cohorts.preview_cohort2')
    def preview_cohort2(self, request):
        """
        Takes a JSON object of filters in the request body and returns a "preview" of the cohort that would
        result from passing a similar request to the cohort **save** endpoint.  This preview consists of
        two lists: the lists of participant (aka patient) barcodes, and the list of sample barcodes.
        Authentication is not required.
        """
        # print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
        patient_cursor = None
        sample_cursor = None
        db = None

        if cohort_helpers.are_there_bad_keys(request) or cohort_helpers.are_there_no_acceptable_keys(request):
            err_msg = cohort_helpers.construct_parameter_error_message(request, True)
            raise endpoints.BadRequestException(err_msg)

        query_dict = {
            k.name: request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and not k.name.endswith('_gte') and not k.name.endswith('_lte')
            }

        gte_query_dict = {
            k.name.replace('_gte', ''): request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and k.name.endswith('_gte')
            }

        lte_query_dict = {
            k.name.replace('_lte', ''): request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and k.name.endswith('_lte')
            }

        patient_query_str = 'SELECT DISTINCT(IF(ParticipantBarcode="", LEFT(SampleBarcode,12), ParticipantBarcode)) ' \
                            'AS ParticipantBarcode ' \
                            'FROM metadata_samples ' \
                            'WHERE '

        sample_query_str = 'SELECT SampleBarcode ' \
                           'FROM metadata_samples ' \
                           'WHERE '

        value_tuple = ()

        for key, value_list in query_dict.iteritems():

            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            if "None" in value_list:
                value_list.remove("None")
                patient_query_str += ' ( {key} is null '.format(key=key)
                sample_query_str += ' ( {key} is null '.format(key=key)
                if len(value_list) > 0:
                    patient_query_str += ' OR {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
                    sample_query_str += ' OR {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
                patient_query_str += ') '
                sample_query_str += ') '
            else:
                patient_query_str += ' {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
                sample_query_str += ' {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
            value_tuple += tuple(value_list)

        for key, value in gte_query_dict.iteritems():
            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            patient_query_str += ' {} >=%s '.format(key)
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            sample_query_str += ' {} >=%s '.format(key)
            value_tuple += (value,)

        for key, value in lte_query_dict.iteritems():
            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            patient_query_str += ' {} <=%s '.format(key)
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            sample_query_str += ' {} <=%s '.format(key)
            value_tuple += (value,)

        sample_query_str += ' GROUP BY SampleBarcode'

        patient_barcodes = []
        sample_barcodes = []

        try:
            db = sql_connection()
            patient_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            patient_cursor.execute(patient_query_str, value_tuple)
            for row in patient_cursor.fetchall():
                patient_barcodes.append(row['ParticipantBarcode'])

            sample_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            sample_cursor.execute(sample_query_str, value_tuple)
            for row in sample_cursor.fetchall():
                sample_barcodes.append(row['SampleBarcode'])

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException("Error retrieving samples or patients: {}".format(e))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\tpatient query: {} {}\n\tsample query: {} {}' \
                .format(e, patient_query_str, value_tuple, sample_query_str, value_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error previewing cohort. {}".format(msg))
        finally:
            if patient_cursor: patient_cursor.close()
            if sample_cursor: sample_cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)

        return CohortPatientsSamplesList(patients=patient_barcodes,
                                         patient_count=len(patient_barcodes),
                                         samples=sample_barcodes,
                                         sample_count=len(sample_barcodes))
