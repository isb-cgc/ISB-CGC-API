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

from isb_cgc_api_helpers import ISB_CGC_TCGA_Endpoints, build_constructor_dict_for_message, \
    CohortsSamplesFilesMessageBuilder
from message_classes import MetadataItem
from api_3.api_helpers import sql_connection

logger = logging.getLogger(__name__)


class SamplesGetQueryBuilder(object):

    def build_aliquot_query(self, platform=None, pipeline=None):

        aliquot_query_str = 'select AliquotBarcode ' \
                            'from metadata_data ' \
                            'where sample_barcode=%s '

        aliquot_query_str += ' and platform=%s ' if platform is not None else ''
        aliquot_query_str += ' and pipeline=%s ' if pipeline is not None else ''
        aliquot_query_str += ' group by AliquotBarcode'

        return aliquot_query_str

    def build_biospecimen_query(self):

        biospecimen_query_str = 'select * ' \
                                'from metadata_biospecimen ' \
                                'where sample_barcode=%s'

        return biospecimen_query_str

    def build_data_query(self, platform=None, pipeline=None):

        data_query_str = 'select ' \
                         'sample_barcode, ' \
                         'DataCenterName, ' \
                         'DataCenterType, ' \
                         'DataFileName, ' \
                         'DataFileNameKey, ' \
                         'DatafileUploaded, ' \
                         'DataLevel,' \
                         'Datatype,' \
                         'GenomeReference,' \
                         'Pipeline,' \
                         'Platform,' \
                         'platform_full_name,' \
                         'program_name,' \
                         'Repository,' \
                         'SDRFFileName,' \
                         'SecurityProtocol ' \
                         'from metadata_data ' \
                         'where sample_barcode=%s ' \
                         'and DataFileNameKey is not null and DataFileNameKey !=""'

        data_query_str += ' and platform=%s ' if platform is not None else ''
        data_query_str += ' and pipeline=%s ' if pipeline is not None else ''

        return data_query_str

    def build_patient_query(self):

        patient_query_str = 'select case_barcode ' \
                            'from metadata_biospecimen ' \
                            'where sample_barcode=%s ' \
                            'group by case_barcode'

        return patient_query_str


class DataDetails(messages.Message):
    sample_Barcode = messages.StringField(1)
    DataCenterName = messages.StringField(2)
    DataCenterType = messages.StringField(3)
    DataFileName = messages.StringField(4)
    DataFileNameKey = messages.StringField(5)
    DatafileUploaded = messages.StringField(6)
    DataLevel = messages.StringField(7)
    Datatype = messages.StringField(8)
    GenomeReference = messages.StringField(9)
    Pipeline = messages.StringField(10)
    Platform = messages.StringField(11)
    platform_full_name = messages.StringField(12)
    Project = messages.StringField(13)
    Repository = messages.StringField(14)
    SDRFFileName = messages.StringField(15)
    SecurityProtocol = messages.StringField(16)
    cloud_storage_path = messages.StringField(17)


class SampleDetails(messages.Message):
    biospecimen_data = messages.MessageField(MetadataItem, 1)
    aliquots = messages.StringField(2, repeated=True)
    patient = messages.StringField(3)
    data_details = messages.MessageField(DataDetails, 4, repeated=True)
    data_details_count = messages.IntegerField(5, variant=messages.Variant.INT32)


@ISB_CGC_TCGA_Endpoints.api_class(resource_name='samples')
class SamplesGetAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True),
                                               platform=messages.StringField(2),
                                               pipeline=messages.StringField(3))

    @endpoints.method(GET_RESOURCE, SampleDetails,
                      path='samples/{sample_barcode}', http_method='GET')
    def get(self, request):
        """
        Given a sample barcode (of length 16, *eg* TCGA-B9-7268-01A), this endpoint returns
        all available "biospecimen" information about this sample,
        the associated patient barcode, a list of associated aliquots,
        and a list of "data_details" blocks describing each of the data files associated with this sample
        """

        cursor = None
        db = None

        sample_barcode = request.get_assigned_value('sample_barcode')
        pipeline = request.get_assigned_value('pipeline')
        platform = request.get_assigned_value('platform')

        aliquot_query_str = SamplesGetQueryBuilder().build_aliquot_query(platform=platform, pipeline=pipeline)
        biospecimen_query_str = SamplesGetQueryBuilder().build_biospecimen_query()
        data_query_str = SamplesGetQueryBuilder().build_data_query(platform=platform, pipeline=pipeline)
        patient_query_str = SamplesGetQueryBuilder().build_patient_query()

        query_tuple = (str(sample_barcode),)
        extra_query_tuple = query_tuple
        if pipeline is not None: extra_query_tuple += (pipeline,)
        if platform is not None: extra_query_tuple += (platform,)

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build biospecimen data message
            cursor.execute(biospecimen_query_str, query_tuple)
            row = cursor.fetchone()
            if row is None:
                cursor.close()
                db.close()
                error_message = "Sample barcode {} not found in metadata_biospecimen table.".format(sample_barcode)
                raise endpoints.NotFoundException(error_message)
            constructor_dict = build_constructor_dict_for_message(MetadataItem(), row)
            biospecimen_data_item = MetadataItem(**constructor_dict)

            # get list of aliquots
            cursor.execute(aliquot_query_str, extra_query_tuple)
            aliquot_list = [row['AliquotBarcode'] for row in cursor.fetchall()]

            # get patient barcode (superfluous?)
            cursor.execute(patient_query_str, query_tuple)
            row = cursor.fetchone()
            patient_barcode = str(row["case_barcode"])

            # prepare to build list of data details messages
            cursor.execute(data_query_str, extra_query_tuple)
            cursor_rows = cursor.fetchall()
            # update every dictionary in cursor_rows to contain the full cloud_storage_path for each sample
            bad_repo_count, bad_repo_set = \
                CohortsSamplesFilesMessageBuilder().get_GCS_file_paths_and_bad_repos(cursor_rows)
            if bad_repo_count > 0:
                logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                            .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))

            # build a data details message for each row returned from metadata_data table
            data_details_list = []
            for row in cursor_rows:
                constructor_dict = build_constructor_dict_for_message(DataDetails(), row)
                data_details_item = DataDetails(**constructor_dict)
                data_details_list.append(data_details_item)

            if bad_repo_count > 0:
                logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                            .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))

            return SampleDetails(aliquots=aliquot_list,
                                 biospecimen_data=biospecimen_data_item,
                                 data_details=data_details_list,
                                 data_details_count=len(data_details_list),
                                 patient=patient_barcode)

        except (IndexError, TypeError) as e:
            logger.info("Sample details for barcode {} not found. Error: {}".format(sample_barcode, e))
            raise endpoints.NotFoundException(
                "Sample details for barcode {} not found.".format(sample_barcode))
        except MySQLdb.ProgrammingError as e:
            logger.warn(e)
            raise endpoints.BadRequestException("Error retrieving biospecimen, patient, or other data. {}".format(e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()