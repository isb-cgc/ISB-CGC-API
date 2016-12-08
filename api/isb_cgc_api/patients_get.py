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

from django.core.signals import request_finished
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints, build_constructor_dict_for_message
from message_classes import MetadataItem
from api.api_helpers import sql_connection

logger = logging.getLogger(__name__)


class PatientsGetQueryBuilder(object):

    def build_queries(self):
        clinical_query_str = 'select * ' \
                             'from metadata_clinical ' \
                             'where case_barcode=%s'

        sample_query_str = 'select SampleBarcode as sample_barcode' \
                           'from metadata_biospecimen ' \
                           'where case_barcode=%s'

        aliquot_query_str = 'select AliquotBarcode ' \
                            'from metadata_data ' \
                            'where case_barcode=%s ' \
                            'group by AliquotBarcode'

        return clinical_query_str, sample_query_str, aliquot_query_str


class PatientDetails(messages.Message):
    clinical_data = messages.MessageField(MetadataItem, 1)
    samples = messages.StringField(2, repeated=True)
    aliquots = messages.StringField(3, repeated=True)


@ISB_CGC_Endpoints.api_class(resource_name='patients')
class PatientsGetAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(patient_barcode=messages.StringField(1, required=True))

    @endpoints.method(GET_RESOURCE, PatientDetails,
                      path='patients/{patient_barcode}', http_method='GET')
    def get(self, request):
        """
        Returns information about a specific patient,
        including a list of samples and aliquots derived from this patient.
        Takes a patient barcode (of length 12, *eg* TCGA-B9-7268) as a required parameter.
        User does not need to be authenticated.
        """

        cursor = None
        db = None

        patient_barcode = request.get_assigned_value('patient_barcode')
        query_tuple = (str(patient_barcode),)
        clinical_query_str, sample_query_str, aliquot_query_str = PatientsGetQueryBuilder().build_queries()

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build clinical data message
            cursor.execute(clinical_query_str, query_tuple)
            row = cursor.fetchone()
            if row is None:
                cursor.close()
                db.close()
                logger.warn("Patient barcode {} not found in metadata_clinical table.".format(patient_barcode))
                raise endpoints.NotFoundException("Patient barcode {} not found".format(patient_barcode))
            constructor_dict = build_constructor_dict_for_message(MetadataItem(), row)
            clinical_data_item = MetadataItem(**constructor_dict)

            # get list of samples
            cursor.execute(sample_query_str, query_tuple)
            sample_list = [row['sample_barcode'] for row in cursor.fetchall()]

            # get list of aliquots
            cursor.execute(aliquot_query_str, query_tuple)
            aliquot_list = [row['AliquotBarcode'] for row in cursor.fetchall()]

            return PatientDetails(clinical_data=clinical_data_item, samples=sample_list, aliquots=aliquot_list)

        except (IndexError, TypeError), e:
            logger.info("Patient {} not found. Error: {}".format(patient_barcode, e))
            raise endpoints.NotFoundException("Patient {} not found.".format(patient_barcode))
        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving patient, sample, or aliquot data: {}".format(e))
            raise endpoints.BadRequestException("Error retrieving patient, sample, or aliquot data: {}".format(e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)