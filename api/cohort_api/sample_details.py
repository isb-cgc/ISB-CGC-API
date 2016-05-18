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

from cohort_helpers import Cohort_Endpoints
from api.api_helpers import sql_connection
from api.metadata import MetadataItem

logger = logging.getLogger(__name__)


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
    data_details_count = messages.IntegerField(5)
    error = messages.StringField(6)


@Cohort_Endpoints.api_class(resource_name='cohort_endpoints')
class SampleDetails(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(patient_barcode=messages.StringField(1, required=True))

    @endpoints.method(GET_RESOURCE, SampleDetails,
                      path='sample_details2', http_method='GET', name='cohorts.sample_details2')
    def sample_details2(self, request):
        """
        Given a sample barcode (of length 16, *eg* TCGA-B9-7268-01A), this endpoint returns
        all available "biospecimen" information about this sample,
        the associated patient barcode, a list of associated aliquots,
        and a list of "data_details" blocks describing each of the data files associated with this sample
        """

        biospecimen_cursor = None
        aliquot_cursor = None
        patient_cursor = None
        data_cursor = None
        db = None

        sample_barcode = request.get_assigned_value('sample_barcode')
        biospecimen_query_str = 'select * ' \
                                'from metadata_biospecimen ' \
                                'where SampleBarcode=%s'

        query_tuple = (str(sample_barcode),)
        extra_query_tuple = query_tuple

        aliquot_query_str = 'select AliquotBarcode ' \
                            'from metadata_data ' \
                            'where SampleBarcode=%s '

        patient_query_str = 'select ParticipantBarcode ' \
                            'from metadata_biospecimen ' \
                            'where SampleBarcode=%s '

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

        if request.get_assigned_value('platform') is not None:
            platform = request.get_assigned_value('platform')
            aliquot_query_str += ' and platform=%s '
            data_query_str += ' and platform=%s '
            extra_query_tuple += (str(platform),)

        if request.get_assigned_value('pipeline') is not None:
            pipeline = request.get_assigned_value('pipeline')
            aliquot_query_str += ' and pipeline=%s '
            data_query_str += ' and pipeline=%s '
            extra_query_tuple += (str(pipeline),)

        aliquot_query_str += ' group by AliquotBarcode'
        patient_query_str += ' group by ParticipantBarcode'

        try:
            db = sql_connection()
            biospecimen_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            biospecimen_cursor.execute(biospecimen_query_str, query_tuple)
            row = biospecimen_cursor.fetchone()

            item = MetadataItem(
                avg_percent_lymphocyte_infiltration=None if "avg_percent_lymphocyte_infiltration" not in row or row[
                                                                                                                    "avg_percent_lymphocyte_infiltration"] is None else float(
                    row["avg_percent_lymphocyte_infiltration"]),
                avg_percent_monocyte_infiltration=None if "avg_percent_monocyte_infiltration" not in row or row[
                                                                                                                "avg_percent_monocyte_infiltration"] is None else float(
                    row["avg_percent_monocyte_infiltration"]),
                avg_percent_necrosis=None if "avg_percent_necrosis" not in row or row[
                                                                                      "avg_percent_necrosis"] is None else float(
                    row["avg_percent_necrosis"]),
                avg_percent_neutrophil_infiltration=None if "avg_percent_neutrophil_infiltration" not in row or row[
                                                                                                                    "avg_percent_neutrophil_infiltration"] is None else float(
                    row["avg_percent_neutrophil_infiltration"]),
                avg_percent_normal_cells=None if "avg_percent_normal_cells" not in row or row[
                                                                                              "avg_percent_normal_cells"] is None else float(
                    row["avg_percent_normal_cells"]),
                avg_percent_stromal_cells=None if "avg_percent_stromal_cells" not in row or row[
                                                                                                "avg_percent_stromal_cells"] is None else float(
                    row["avg_percent_stromal_cells"]),
                avg_percent_tumor_cells=None if "avg_percent_tumor_cells" not in row or row[
                                                                                            "avg_percent_tumor_cells"] is None else float(
                    row["avg_percent_tumor_cells"]),
                avg_percent_tumor_nuclei=None if "avg_percent_tumor_nuclei" not in row or row[
                                                                                              "avg_percent_tumor_nuclei"] is None else float(
                    row["avg_percent_tumor_nuclei"]),
                batch_number=None if "batch_number" not in row or row["batch_number"] is None else int(
                    row["batch_number"]),
                bcr=str(row["bcr"]),
                days_to_collection=None if "days_to_collection" not in row or row[
                                                                                  'days_to_collection'] is None else int(
                    row["days_to_collection"]),
                max_percent_lymphocyte_infiltration=None if "max_percent_lymphocyte_infiltration" not in row or row[
                                                                                                                    "max_percent_lymphocyte_infiltration"] is None else int(
                    row["max_percent_lymphocyte_infiltration"]),  # 46)
                max_percent_monocyte_infiltration=None if "max_percent_monocyte_infiltration" not in row or row[
                                                                                                                "max_percent_monocyte_infiltration"] is None else int(
                    row["max_percent_monocyte_infiltration"]),  # 47)
                max_percent_necrosis=None if "max_percent_necrosis" not in row or row[
                                                                                      "max_percent_necrosis"] is None else int(
                    row["max_percent_necrosis"]),  # 48)
                max_percent_neutrophil_infiltration=None if "max_percent_neutrophil_infiltration" not in row or row[
                                                                                                                    "max_percent_neutrophil_infiltration"] is None else int(
                    row["max_percent_neutrophil_infiltration"]),  # 49)
                max_percent_normal_cells=None if "max_percent_normal_cells" not in row or row[
                                                                                              "max_percent_normal_cells"] is None else int(
                    row["max_percent_normal_cells"]),  # 50)
                max_percent_stromal_cells=None if "max_percent_stromal_cells" not in row or row[
                                                                                                "max_percent_stromal_cells"] is None else int(
                    row["max_percent_stromal_cells"]),  # 51)
                max_percent_tumor_cells=None if "max_percent_tumor_cells" not in row or row[
                                                                                            "max_percent_tumor_cells"] is None else int(
                    row["max_percent_tumor_cells"]),  # 52)
                max_percent_tumor_nuclei=None if "max_percent_tumor_nuclei" not in row or row[
                                                                                              "max_percent_tumor_nuclei"] is None else int(
                    row["max_percent_tumor_nuclei"]),  # 53)
                min_percent_lymphocyte_infiltration=None if "min_percent_lymphocyte_infiltration" not in row or row[
                                                                                                                    "min_percent_lymphocyte_infiltration"] is None else int(
                    row["min_percent_lymphocyte_infiltration"]),  # 55)
                min_percent_monocyte_infiltration=None if "min_percent_monocyte_infiltration" not in row or row[
                                                                                                                "min_percent_monocyte_infiltration"] is None else int(
                    row["min_percent_monocyte_infiltration"]),  # 56)
                min_percent_necrosis=None if "min_percent_necrosis" not in row or row[
                                                                                      "min_percent_necrosis"] is None else int(
                    row["min_percent_necrosis"]),  # 57)
                min_percent_neutrophil_infiltration=None if "min_percent_neutrophil_infiltration" not in row or row[
                                                                                                                    "min_percent_neutrophil_infiltration"] is None else int(
                    row["min_percent_neutrophil_infiltration"]),  # 58)
                min_percent_normal_cells=None if "min_percent_normal_cells" not in row or row[
                                                                                              "min_percent_normal_cells"] is None else int(
                    row["min_percent_normal_cells"]),  # 59)
                min_percent_stromal_cells=None if "min_percent_stromal_cells" not in row or row[
                                                                                                "min_percent_stromal_cells"] is None else int(
                    row["min_percent_stromal_cells"]),  # 60)
                min_percent_tumor_cells=None if "min_percent_tumor_cells" not in row or row[
                                                                                            "min_percent_tumor_cells"] is None else int(
                    row["min_percent_tumor_cells"]),  # 61)
                min_percent_tumor_nuclei=None if "min_percent_tumor_nuclei" not in row or row[
                                                                                              "min_percent_tumor_nuclei"] is None else int(
                    row["min_percent_tumor_nuclei"]),  # 62)
                ParticipantBarcode=str(row["ParticipantBarcode"]),
                Project=str(row["Project"]),
                SampleBarcode=str(row["SampleBarcode"]),
                Study=str(row["Study"])
            )
            aliquot_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            aliquot_cursor.execute(aliquot_query_str, extra_query_tuple)
            aliquot_data = []
            for row in aliquot_cursor.fetchall():
                aliquot_data.append(row['AliquotBarcode'])

            patient_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            patient_cursor.execute(patient_query_str, query_tuple)
            row = patient_cursor.fetchone()
            if row is None:
                aliquot_cursor.close()
                patient_cursor.close()
                biospecimen_cursor.close()
                db.close()
                error_message = "Sample barcode {} not found in metadata_biospecimen table.".format(sample_barcode)
                return SampleDetails(biospecimen_data=None, aliquots=[], patient=None, data_details=[],
                                     data_details_count=None, error=error_message)
            patient_barcode = str(row["ParticipantBarcode"])

            data_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            data_cursor.execute(data_query_str, extra_query_tuple)
            data_data = []
            bad_repo_count = 0
            bad_repo_set = set()
            for row in data_cursor.fetchall():
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
            msg = '{}:\n\tbiospecimen query: {} {}\n\tpatient query: {} {}\n\tdata query: {} {}' \
                .format(e, biospecimen_query_str, query_tuple, patient_query_str, query_tuple,
                        data_query_str, extra_query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving biospecimen, patient, or other data. {}".format(msg))
        finally:
            if biospecimen_cursor: biospecimen_cursor.close()
            if aliquot_cursor: aliquot_cursor.close()
            if patient_cursor: patient_cursor.close()
            if data_cursor: data_cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)
