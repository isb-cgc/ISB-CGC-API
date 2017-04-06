'''
Created on Apr 5, 2017

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

@author: michael
'''
import endpoints
import logging
import MySQLdb

from django.core.signals import request_finished
from protorpc import remote, messages

from api_3.cohort_endpoint_helpers import build_constructor_dict_for_message
from api_3.api_helpers import sql_connection

logger = logging.getLogger(__name__)


class CasesGetQueryBuilder(object):

    def build_queries(self):
        clinical_query_str = 'select * ' \
                             'from metadata_clinical ' \
                             'where case_barcode=%s'

        sample_query_str = 'select sample_barcode ' \
                           'from metadata_biospecimen ' \
                           'where case_barcode=%s'

        aliquot_query_str = 'select AliquotBarcode ' \
                            'from metadata_data ' \
                            'where case_barcode=%s ' \
                            'group by AliquotBarcode'

        return clinical_query_str, sample_query_str, aliquot_query_str


class CasesGetHelper(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(case_barcode=messages.StringField(1, required=True))

    def get(self, request, CaseDetails, MetadataItem):
        """
        Returns information about a specific case,
        including a list of samples and aliquots derived from this case.
        Takes a case (*eg* TCGA-B9-7268 for TCGA) as a required parameter.
        User does not need to be authenticated.
        """

        cursor = None
        db = None

        case_barcode = request.get_assigned_value('case_barcode')
        query_tuple = (str(case_barcode),)
        clinical_query_str, sample_query_str, aliquot_query_str = CasesGetQueryBuilder().build_queries()

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build clinical data message
            cursor.execute(clinical_query_str, query_tuple)
            row = cursor.fetchone()
            if row is None:
                cursor.close()
                db.close()
                logger.warn("Case barcode {} not found in metadata_clinical table.".format(case_barcode))
                raise endpoints.NotFoundException("Case barcode {} not found".format(case_barcode))
            constructor_dict = build_constructor_dict_for_message(MetadataItem(), row)
            clinical_data_item = MetadataItem(**constructor_dict)

            # get list of samples
            cursor.execute(sample_query_str, query_tuple)
            sample_list = [row['sample_barcode'] for row in cursor.fetchall()]

            # get list of aliquots
            cursor.execute(aliquot_query_str, query_tuple)
            aliquot_list = [row['AliquotBarcode'] for row in cursor.fetchall()]

            return CaseDetails(clinical_data=clinical_data_item, samples=sample_list, aliquots=aliquot_list)

        except (IndexError, TypeError), e:
            logger.info("Case {} not found. Error: {}".format(case_barcode, e))
            raise endpoints.NotFoundException("Case {} not found.".format(case_barcode))
        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving case, sample, or aliquot data: {}".format(e))
            raise endpoints.BadRequestException("Error retrieving case, sample, or aliquot data: {}".format(e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)
