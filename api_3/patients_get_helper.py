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

    def build_queries(self, program, genomic_builds, count=1):

        clin_case_clause = 'case_barcode=%s'
        case_clause = 'case_barcode=%s'

        if count > 1:
            clin_case_clause = 'case_barcode in ({})'.format(",".join(['%s']*count))

        clinical_query_str = 'select * ' \
                             'from {}_metadata_clinical ' \
                             'where {}'.format(program, clin_case_clause)

        sample_query_str = 'select sample_barcode ' \
                           'from {}_metadata_biospecimen ' \
                           'where {} ' \
                           'group by sample_barcode ' \
                           'order by sample_barcode'.format(program, case_clause)

        aliquot_query_str = ''
        for genomic_build in genomic_builds:
            part_aliquot_query_str = 'select aliquot_barcode ' \
                                'from {}_metadata_data_{} ' \
                                'where {} and aliquot_barcode is not null ' \
                                'group by aliquot_barcode ' \
                                'order by aliquot_barcode'.format(program, genomic_build, case_clause)
            if 0 < len(aliquot_query_str):
                aliquot_query_str += ' union '
            aliquot_query_str += part_aliquot_query_str

        return clinical_query_str, sample_query_str, aliquot_query_str

class CaseGetListFilters(messages.Message):
    case_barcodes = messages.StringField(1, repeated=True)

class CasesGetHelper(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(case_barcode=messages.StringField(1, required=True))

    POST_RESOURCE = endpoints.ResourceContainer(
        filters=messages.MessageField(CaseGetListFilters, 1)
    )

    def get(self, request, CaseDetails, MetadataItem, program):
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
        clinical_query_str, sample_query_str, aliquot_query_str = CasesGetQueryBuilder().build_queries(program, ['HG19'])

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build clinical data message
            cursor.execute(clinical_query_str, query_tuple)
            row = cursor.fetchone()
            if row is None:
                cursor.close()
                db.close()
                logger.warn("Case barcode {} not found in {}_metadata_clinical table.".format(case_barcode, program))
                raise endpoints.NotFoundException("Case barcode {} not found".format(case_barcode))
            constructor_dict = build_constructor_dict_for_message(MetadataItem(), row)
            clinical_data_item = MetadataItem(**constructor_dict)

            # get list of samples
            cursor.execute(sample_query_str, query_tuple)
            sample_list = [row['sample_barcode'] for row in cursor.fetchall()]

            # get list of aliquots
            cursor.execute(aliquot_query_str, query_tuple)
            aliquot_list = [row['aliquot_barcode'] for row in cursor.fetchall()]

            return CaseDetails(clinical_data=clinical_data_item, samples=sample_list, aliquots=aliquot_list if aliquot_list else [])
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


    def get_list(self, request, CaseSetDetails, CaseDetails, MetadataItem, program):
        """
        Returns information about a specific case,
        including a list of samples and aliquots derived from this case.
        Takes a case (*eg* TCGA-B9-7268 for TCGA) as a required parameter.
        User does not need to be authenticated.
        """

        cursor = None
        db = None
        case_barcodes = None

        filter_obj = request.get_assigned_value('filters') if 'filters' in [k.name for k in request.all_fields()] else None

        if filter_obj:
            case_barcodes = filter_obj.get_assigned_value('case_barcodes') if 'case_barcodes' in [k.name for k in filter_obj.all_fields()] else None

        if not case_barcodes or not len(case_barcodes):
            raise endpoints.BadRequestException("A list of case barcodes is required.")
        elif len(case_barcodes) > 500:
            raise endpoints.BadRequestException("The limit on barcodes per request is 500.")

        query_tuple = [x for x in case_barcodes]

        clinical_query_str, sample_query_str, aliquot_query_str = CasesGetQueryBuilder().build_queries(program, ['HG19'], len(case_barcodes))

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build clinical data message
            cursor.execute(clinical_query_str, query_tuple)
            rows = cursor.fetchall()
            if not len(rows):
                cursor.close()
                db.close()
                logger.warn("None of the case barcodes were found in the {}_metadata_clinical table.".format(program))
                raise endpoints.NotFoundException("None of the case barcodes were found")

            case_details = []

            for row in rows:
                constructor_dict = build_constructor_dict_for_message(MetadataItem(), row)
                clinical_data_item = MetadataItem(**constructor_dict)

                # get list of samples
                cursor.execute(sample_query_str, (row['case_barcode'],))
                sample_list = [sample_row['sample_barcode'] for sample_row in cursor.fetchall()]

                # get list of aliquots
                cursor.execute(aliquot_query_str, (row['case_barcode'],))
                aliquot_list = [aliquot_row['aliquot_barcode'] for aliquot_row in cursor.fetchall()]

                case_details.append(CaseDetails(clinical_data=clinical_data_item, samples=sample_list,
                               aliquots=aliquot_list if aliquot_list else []))

            return CaseSetDetails(cases=case_details)
        except (IndexError, TypeError), e:
            logger.info("The cases supplied were not found. Error: {}".format(e))
            raise endpoints.NotFoundException("The cases provided were not found not found.")
        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving case, sample, or aliquot data: {}".format(e))
            raise endpoints.BadRequestException("Error retrieving case, sample, or aliquot data: {}".format(e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)
