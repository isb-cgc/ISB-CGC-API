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

from django.conf import settings
from django.core.signals import request_finished
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints, MetadataItem
from api.api_helpers import sql_connection

logger = logging.getLogger(__name__)


class SamplesGetQueryBuilder(object):

    def build_aliquot_query(self, platform=None, pipeline=None):

        aliquot_query_str = 'select AliquotBarcode ' \
                            'from metadata_data ' \
                            'where SampleBarcode=%s '

        aliquot_query_str += ' and platform=%s ' if platform is not None else ''
        aliquot_query_str += ' and pipeline=%s ' if pipeline is not None else ''
        aliquot_query_str += ' group by AliquotBarcode'

        return aliquot_query_str

    def build_biospecimen_query(self):

        biospecimen_query_str = 'select * ' \
                                'from metadata_biospecimen ' \
                                'where SampleBarcode=%s'

        return biospecimen_query_str

    def build_data_query(self, platform=None, pipeline=None):

        data_query_str = 'select ' \
                         'SampleBarcode, ' \
                         'DataCenterName, ' \
                         'DataCenterType, ' \
                         'DataFileName, ' \
                         'DataFileNameKey, ' \
                         'DatafileUploaded, ' \
                         'DataLevel,' \
                         'Datatype,' \
                         'GenomeReference,' \
                         'GG_dataset_id, ' \
                         'GG_readgroupset_id, ' \
                         'Pipeline,' \
                         'Platform,' \
                         'platform_full_name,' \
                         'Project,' \
                         'Repository,' \
                         'SDRFFileName,' \
                         'SecurityProtocol ' \
                         'from metadata_data ' \
                         'where SampleBarcode=%s '

        data_query_str += ' and platform=%s ' if platform is not None else ''
        data_query_str += ' and pipeline=%s ' if pipeline is not None else ''

        return data_query_str

    def build_patient_query(self):

        patient_query_str = 'select ParticipantBarcode ' \
                            'from metadata_biospecimen ' \
                            'where SampleBarcode=%s ' \
                            'group by ParticipantBarcode'

        return patient_query_str


class DataDetails(messages.Message):
    SampleBarcode = messages.StringField(1)
    DataCenterName = messages.StringField(2)
    DataCenterType = messages.StringField(3)
    DataFileName = messages.StringField(4)
    DataFileNameKey = messages.StringField(5)
    DatafileUploaded = messages.StringField(6)
    DataLevel = messages.StringField(7)
    Datatype = messages.StringField(8)
    GenomeReference = messages.StringField(9)
    GG_dataset_id = messages.StringField(10)
    GG_readgroupset_id = messages.StringField(11)
    Pipeline = messages.StringField(12)
    Platform = messages.StringField(13)
    platform_full_name = messages.StringField(14)
    Project = messages.StringField(15)
    Repository = messages.StringField(16)
    SDRFFileName = messages.StringField(17)
    SecurityProtocol = messages.StringField(18)
    CloudStoragePath = messages.StringField(19)


class SampleDetails(messages.Message):
    biospecimen_data = messages.MessageField(MetadataItem, 1)
    aliquots = messages.StringField(2, repeated=True)
    patient = messages.StringField(3)
    data_details = messages.MessageField(DataDetails, 4, repeated=True)
    data_details_count = messages.IntegerField(5, variant=messages.Variant.INT32)


@ISB_CGC_Endpoints.api_class(resource_name='samples')
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
            cursor.execute(biospecimen_query_str, query_tuple)
            row = cursor.fetchone()

            constructor_dict = {}
            metadata_item_dict = {field.name: field for field in MetadataItem().all_fields()}
            for name, field in metadata_item_dict.iteritems():
                if row.get(name) is not None:
                    try:
                        field.validate(row[name])
                        constructor_dict[name] = row[name]
                    except messages.ValidationError, e:
                        constructor_dict[name] = None
                        print name + ': ' + str(row[name]) + ' was not validated'
                else:
                    constructor_dict[name] = None

            item = MetadataItem(**constructor_dict)


            # aliquot_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(aliquot_query_str, extra_query_tuple)
            aliquot_data = [row['AliquotBarcode'] for row in cursor.fetchall()]

            # patient_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(patient_query_str, query_tuple)
            row = cursor.fetchone()
            if row is None:
                # aliquot_cursor.close()
                # patient_cursor.close()
                # biospecimen_cursor.close()
                cursor.close()
                db.close()
                error_message = "Sample barcode {} not found in metadata_biospecimen table.".format(sample_barcode)
                return SampleDetails(biospecimen_data=None, aliquots=[], patient=None, data_details=[],
                                     data_details_count=None, error=error_message)
            patient_barcode = str(row["ParticipantBarcode"])

            # data_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(data_query_str, extra_query_tuple)

            # todo: replace with CohortsSamplesFilesMessageBuilder().get_files_and_bad_repos(cursor.fetchall())
            data_data = []
            bad_repo_count = 0
            bad_repo_set = set()
            for row in cursor.fetchall():
                if not row.get('DataFileNameKey'):
                    continue
                if 'controlled' not in str(row['SecurityProtocol']).lower():
                    cloud_storage_path = "gs://{}{}".format(settings.OPEN_DATA_BUCKET, row.get('DataFileNameKey'))
                else:  # not filtering on dbGaP_authorized:
                    if row['Repository'].lower() == 'dcc':
                        bucket_name = settings.DCC_CONTROLLED_DATA_BUCKET
                    elif row['Repository'].lower() == 'cghub':
                        bucket_name = settings.CGHUB_CONTROLLED_DATA_BUCKET
                    else:  # shouldn't ever happen
                        bad_repo_count += 1
                        bad_repo_set.add(row['Repository'])
                        continue
                    cloud_storage_path = "gs://{}{}".format(bucket_name, row.get('DataFileNameKey'))

                data_item = DataDetails(
                    SampleBarcode=str(row['SampleBarcode']),
                    DataCenterName=str(row['DataCenterName']),
                    DataCenterType=str(row['DataCenterType']),
                    DataFileName=str(row['DataFileName']),
                    DataFileNameKey=str(row.get('DataFileNameKey')),
                    DatafileUploaded=str(row['DatafileUploaded']),
                    DataLevel=str(row['DataLevel']),
                    Datatype=str(row['Datatype']),
                    GenomeReference=str(row['GenomeReference']),
                    GG_dataset_id=str(row['GG_dataset_id']),
                    GG_readgroupset_id=str(row['GG_readgroupset_id']),
                    Pipeline=str(row['Pipeline']),
                    Platform=str(row['Platform']),
                    platform_full_name=str(row['platform_full_name']),
                    Project=str(row['Project']),
                    Repository=str(row['Repository']),
                    SDRFFileName=str(row['SDRFFileName']),
                    SecurityProtocol=str(row['SecurityProtocol']),
                    CloudStoragePath=cloud_storage_path
                )
                data_data.append(data_item)
            if bad_repo_count > 0:
                logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                            .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))
            return SampleDetails(biospecimen_data=item, aliquots=aliquot_data,
                                 patient=patient_barcode, data_details=data_data,
                                 data_details_count=len(data_data))

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