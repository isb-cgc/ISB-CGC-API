'''
Created on Apr 5, 2017

opyright 2015, Institute for Systems Biology

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
from protorpc import remote, messages
from api_3.isb_cgc_api_TCGA.message_classes import BiospecimenMetadataItem

from api_3.api_helpers import sql_connection
from api_3.cohort_endpoint_helpers import build_constructor_dict_for_message

logger = logging.getLogger(__name__)

class SamplesGetQueryBuilder(object):
    def build_aliquot_query(self, program, param_list, count=1):
        if 'CCLE' == program:
            genomic_builds = ['HG19']
        else:
            genomic_builds = ['HG19', 'HG38']
            
        aliquot_query_str = ''
        for genomic_build in genomic_builds:
            part_aliquot_query_str = 'select sample_barcode, case_barcode, aliquot_barcode, aliquot_gdc_id ' \
                             'from {}_metadata_data_{}_r14 ' \
                             'where file_name_key is not null and file_name_key !="" '.format(program, genomic_build)
            for column in param_list:
                if column == 'sample_barcode' and count>1:
                    part_aliquot_query_str += ' and {} IN ({}) '.format(column, ','.join(["%s"]*count))
                else:
                    part_aliquot_query_str += ' and {}=%s '.format(column)
            if 0 < len(aliquot_query_str):
                aliquot_query_str += ' union '
            aliquot_query_str += part_aliquot_query_str

        return aliquot_query_str

    def build_biospecimen_query(self, program, count=1):

        biospecimen_query_str = 'select * ' \
                                'from {}_metadata_biospecimen ' \
                                'where sample_barcode=%s'.format(program)
        if count>1:
            biospecimen_query_str = 'select * ' \
                                    'from {}_metadata_biospecimen ' \
                                    'where sample_barcode in ({})'.format(program, ','.join(["%s"] * count))

        return biospecimen_query_str

    def build_data_query(self, program, datadict_class, param_list, count=1):
        if 'CCLE' == program:
            genomic_builds = ['HG19']
        else:
            genomic_builds = ['HG19', 'HG38']
            
        data_query_str = ''
        for genomic_build in genomic_builds:
            part_data_query_str = 'select {0} ' \
                             'from {1}_metadata_data_{2}_r14 ' \
                             'where file_name_key is not null and file_name_key !="" '.format(', '.join(field.name for field in datadict_class.all_fields()), program, genomic_build)
            for column in param_list:
                if column == 'sample_barcode' and count > 1:
                    part_data_query_str += ' and {} IN ({}) '.format(column, ','.join(["%s"]*count))
                else:
                    part_data_query_str += ' and {}=%s '.format(column)
            if 0 < len(data_query_str):
                data_query_str += ' union '
            data_query_str += part_data_query_str

        return data_query_str

    def build_case_query(self, program, count=1):

        case_query_str = 'select case_barcode, case_gdc_id ' \
                            'from {}_metadata_biospecimen ' \
                            'where sample_barcode=%s ' \
                            'group by case_barcode, case_gdc_id'.format(program)

        if count>1:
            case_query_str = 'select case_barcode, case_gdc_id ' \
                             'from {}_metadata_biospecimen ' \
                             'where sample_barcode in ({}) ' \
                             'group by case_barcode, case_gdc_id'.format(program, ','.join(["%s"] * count))

        return case_query_str


class DataDetails(messages.Message):
    file_gdc_id = messages.StringField(1)
    file_name_key = messages.StringField(3)
    file_size = messages.IntegerField(4, variant=messages.Variant.INT64)
    sample_gdc_id = messages.StringField(5)
    sample_barcode = messages.StringField(6)
    project_short_name = messages.StringField(8)
    disease_code = messages.StringField(9)
    program_name = messages.StringField(11)
    data_type = messages.StringField(12)
    data_category = messages.StringField(13)
    experimental_strategy = messages.StringField(14)
    data_format = messages.StringField(15)
    access = messages.StringField(16)
    platform = messages.StringField(17)
    index_file_name_key = messages.StringField(20)


class SampleGetListFilters(messages.Message):
    sample_barcodes = messages.StringField(1, repeated=True)
    disease_code = messages.StringField(2, repeated=True)
    experimental_strategy = messages.StringField(3, repeated=True)
    platform = messages.StringField(4, repeated=True)
    data_category = messages.StringField(5, repeated=True)
    data_type = messages.StringField(6, repeated=True)
    data_format = messages.StringField(7, repeated=True)
    project_short_name = messages.StringField(8, repeated=True)


class SamplesGetAPI(remote.Service):
    GET_RESOURCE = endpoints.ResourceContainer(
        sample_barcode=messages.StringField(1, required=True),
        data_type = messages.StringField(2),
        data_category = messages.StringField(3),
        experimental_strategy = messages.StringField(4),
        data_format = messages.StringField(5),
        platform = messages.StringField(6),
        endpoint_type = messages.StringField(7),
        analysis_workflow_type = messages.StringField(8)
    )

    POST_RESOURCE = endpoints.ResourceContainer(
        SampleGetListFilters
    )

    def get(self, request, program, SampleDetails, MetadataItem):
        """
        Given a sample barcode (of length 16, *eg* TCGA-B9-7268-01A, for TCGA), this endpoint returns
        all available "biospecimen" information about this sample,
        the associated case barcode, a list of associated aliquots,
        and a list of "data_details" blocks describing each of the data files associated with this sample
        """
        cursor = None
        db = None

        sample_barcode = request.get_assigned_value('sample_barcode')
        param_list = ['sample_barcode']
        query_tuple = [sample_barcode]
        extra_query_tuple = [sample_barcode]
        for field in request.all_fields():
            if 'sample_barcode' != field.name and request.get_assigned_value(field.name):
                param_list += [field.name]
                extra_query_tuple += [request.get_assigned_value(field.name)]

        if 'CCLE' != program:
            extra_query_tuple += extra_query_tuple
            
        # need to take into account params used in the union between the genomic builds
        
        aliquot_query_str = SamplesGetQueryBuilder().build_aliquot_query(program, param_list)
        biospecimen_query_str = SamplesGetQueryBuilder().build_biospecimen_query(program)
        data_query_str = SamplesGetQueryBuilder().build_data_query(program, DataDetails(), param_list)
        case_query_str = SamplesGetQueryBuilder().build_case_query(program)

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build biospecimen data message
            cursor.execute(biospecimen_query_str, query_tuple)
            row = cursor.fetchone()
            if row is None:
                cursor.close()
                db.close()
                error_message = "Sample barcode {} not found in {}_metadata_biospecimen table.".format(query_tuple[0], program)
                raise endpoints.NotFoundException(error_message)
            constructor_dict = build_constructor_dict_for_message(MetadataItem(), row)
            biospecimen_data_item = MetadataItem(**constructor_dict)

            # get list of aliquots
            # cursor.execute(aliquot_query_str, extra_query_tuple)
            # aliquot_list = [row['aliquot_barcode'] for row in cursor.fetchall()]

            # get case barcode (superfluous?)
            cursor.execute(case_query_str, query_tuple)
            row = cursor.fetchone()
            case_barcode = str(row["case_barcode"])
            case_gdc_id = str(row["case_gdc_id"])

            # prepare to build list of data details messages
            cursor.execute(data_query_str, extra_query_tuple)
            cursor_rows = cursor.fetchall()

            # build a data details message for each row returned from metadata_data table
            data_details_list = []
            for row in cursor_rows:
                constructor_dict = build_constructor_dict_for_message(DataDetails(), row)
                data_details_item = DataDetails(**constructor_dict)
                data_details_list.append(data_details_item)

            return SampleDetails(aliquots=aliquot_list,
                                 biospecimen_data=biospecimen_data_item,
                                 data_details=data_details_list,
                                 data_details_count=len(data_details_list),
                                 case_barcode=case_barcode,
                                 case_gdc_id=case_gdc_id)

        except (IndexError, TypeError) as e:
            logger.info("Sample details for barcode {} not found. Error: {}, \nSQL: {}, \nParams: {}".format(sample_barcode, e, aliquot_query_str, extra_query_tuple))
            raise endpoints.NotFoundException(
                "Sample details for barcode {} not found.".format(sample_barcode))
        except MySQLdb.ProgrammingError as e:
            logger.warn(e)
            raise endpoints.BadRequestException("Error retrieving biospecimen, case, or other data. {}".format(e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()

    def get_list(self, request, program, SampleSetDetails, SampleDetails, MetadataItem):
        """
        Given a set of sample barcodes (of length 16, *eg* TCGA-B9-7268-01A, for TCGA), this endpoint returns
        all available "biospecimen" information about these samples, the associated case barcodes,
        a list of associated aliquots, and a list of "data_details" blocks describing each of the data files
        associated with this sample
        """
        cursor = None
        db = None
        sample_barcodes = request.get_assigned_value('sample_barcodes') if 'sample_barcodes' in [k.name for k in
            request.all_fields()] else None

        if not sample_barcodes:
            raise endpoints.BadRequestException("A list of sample barcodes is required.")
        elif len(sample_barcodes) > 500:
            raise endpoints.BadRequestException("There is a 500 barcode limit per quest.")

        param_list = ['sample_barcode']
        query_tuple = [x for x in sample_barcodes]
        extra_query_tuple = [x for x in sample_barcodes]
        for field in request.all_fields():
            if 'sample_barcodes' not in field.name and request.get_assigned_value(field.name):
                param_list += [field.name]
                extra_query_tuple += [request.get_assigned_value(field.name)]

        if 'CCLE' != program:
            extra_query_tuple += extra_query_tuple

        # need to take into account params used in the union between the genomic builds

        aliquot_query_str = SamplesGetQueryBuilder().build_aliquot_query(program, param_list, len(sample_barcodes))
        biospecimen_query_str = SamplesGetQueryBuilder().build_biospecimen_query(program, len(sample_barcodes))
        data_query_str = SamplesGetQueryBuilder().build_data_query(program, DataDetails(), param_list, len(sample_barcodes))

        samples = SampleSetDetails()

        sample_data = {}

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build biospecimen data message
            cursor.execute(biospecimen_query_str, query_tuple)
            rows = cursor.fetchall()
            if not len(rows):
                cursor.close()
                db.close()
                error_message = "These sample barcodes were not found in the {}_metadata_biospecimen table.".format(program,)
                raise endpoints.NotFoundException(error_message)

            for row in rows:
                sample_data[row['sample_barcode']] = {}
                constructor_dict = build_constructor_dict_for_message(MetadataItem(), row)
                biospecimen_data_item = MetadataItem(**constructor_dict)
                sample_data[row['sample_barcode']]['biospecimen'] = biospecimen_data_item
                sample_data[row['sample_barcode']]['case_barcode'] = row['case_barcode']
                sample_data[row['sample_barcode']]['case_gdc_id'] = row['case_gdc_id']

            # get list of aliquots
            # cursor.execute(aliquot_query_str, extra_query_tuple)
            # rows = cursor.fetchall()
            # for row in rows:
            #     if 'aliquots' not in sample_data[row['sample_barcode']]:
            #         sample_data[row['sample_barcode']]['aliquots'] = []
            #     sample_data[row['sample_barcode']]['aliquots'].append(row['aliquot_barcode'])

            # prepare to build list of data details messages
            cursor.execute(data_query_str, extra_query_tuple)
            cursor_rows = cursor.fetchall()

            # build a data details message for each row returned from metadata_data table
            for row in cursor_rows:
                if 'data_rows' not in sample_data[row['sample_barcode']]:
                    sample_data[row['sample_barcode']]['data_rows'] = []
                constructor_dict = build_constructor_dict_for_message(DataDetails(), row)
                data_details_item = DataDetails(**constructor_dict)
                sample_data[row['sample_barcode']]['data_rows'].append(data_details_item)

            for sample in sample_data:
                samples.samples.append(
                    SampleDetails(
                        aliquots=sample_data[sample]['aliquots'] if 'aliquots' in sample_data[sample] else [],
                         biospecimen_data=sample_data[sample]['biospecimen'],
                         data_details=sample_data[sample]['data_rows'] if 'data_rows' in sample_data[sample] else [],
                         data_details_count=len(sample_data[sample]['data_rows']) if 'data_rows' in sample_data[sample] else 0,
                         case_barcode=sample_data[sample]['case_barcode'],
                         case_gdc_id=sample_data[sample]['case_gdc_id'],
                         sample_barcode=sample
                    )
                )

            return samples

        except (IndexError, TypeError) as e:
            logger.exception(e)
            logger.error("Error: {}, \nSQL: {}, \nParams: {}".format(e,aliquot_query_str,extra_query_tuple))
            raise endpoints.NotFoundException(
                "There was an error while processing your request--please contact us at feedback@isb-cgc.org"
            )
        except MySQLdb.ProgrammingError as e:
            logger.warn(e)
            raise endpoints.BadRequestException("Error retrieving biospecimen, case, or other data. {}".format(e))
        except Exception as e:
            logger.error("[ERROR] While processing samples.get_list: ")
            logger.exception(e)
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
