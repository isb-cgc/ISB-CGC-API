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

from isb_cgc_api_helpers import ISB_CGC_Endpoints
from api.api_helpers import sql_connection
from api.metadata import MetadataItem

logger = logging.getLogger(__name__)


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

        clinical_cursor = None
        sample_cursor = None
        aliquot_cursor = None
        db = None

        patient_barcode = request.get_assigned_value('patient_barcode')

        clinical_query_str = 'select * ' \
                             'from metadata_clinical ' \
                             'where ParticipantBarcode=%s'

        query_tuple = (str(patient_barcode),)

        sample_query_str = 'select SampleBarcode ' \
                           'from metadata_biospecimen ' \
                           'where ParticipantBarcode=%s'

        aliquot_query_str = 'select AliquotBarcode ' \
                            'from metadata_data ' \
                            'where ParticipantBarcode=%s ' \
                            'group by AliquotBarcode'
        try:
            db = sql_connection()
            clinical_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            clinical_cursor.execute(clinical_query_str, query_tuple)
            row = clinical_cursor.fetchone()

            item = MetadataItem(
                age_at_initial_pathologic_diagnosis=None if "age_at_initial_pathologic_diagnosis" not in row or row[
                                                                                                                    "age_at_initial_pathologic_diagnosis"] is None else int(
                    row["age_at_initial_pathologic_diagnosis"]),
                anatomic_neoplasm_subdivision=str(row["anatomic_neoplasm_subdivision"]),
                batch_number=None if "batch_number" not in row or row["batch_number"] is None else int(
                    row["batch_number"]),
                bcr=str(row["bcr"]),
                clinical_M=str(row["clinical_M"]),
                clinical_N=str(row["clinical_N"]),
                clinical_stage=str(row["clinical_stage"]),
                clinical_T=str(row["clinical_T"]),
                colorectal_cancer=str(row["colorectal_cancer"]),
                country=str(row["country"]),
                days_to_birth=None if "days_to_birth" not in row or row['days_to_birth'] is None else int(
                    row["days_to_birth"]),
                days_to_death=None if "days_to_death" not in row or row['days_to_death'] is None else int(
                    row["days_to_death"]),
                days_to_initial_pathologic_diagnosis=None if "days_to_initial_pathologic_diagnosis" not in row or row[
                                                                                                                      'days_to_initial_pathologic_diagnosis'] is None else int(
                    row["days_to_initial_pathologic_diagnosis"]),
                days_to_last_followup=None if "days_to_last_followup" not in row or row[
                                                                                        'days_to_last_followup'] is None else int(
                    row["days_to_last_followup"]),
                days_to_submitted_specimen_dx=None if "days_to_submitted_specimen_dx" not in row or row[
                                                                                                        'days_to_submitted_specimen_dx'] is None else int(
                    row["days_to_submitted_specimen_dx"]),
                Study=str(row["Study"]),
                ethnicity=str(row["ethnicity"]),
                frozen_specimen_anatomic_site=str(row["frozen_specimen_anatomic_site"]),
                gender=str(row["gender"]),
                height=None if "height" not in row or row['height'] is None else int(row["height"]),
                histological_type=str(row["histological_type"]),
                history_of_colon_polyps=str(row["history_of_colon_polyps"]),
                history_of_neoadjuvant_treatment=str(row["history_of_neoadjuvant_treatment"]),
                history_of_prior_malignancy=str(row["history_of_prior_malignancy"]),
                hpv_calls=str(row["hpv_calls"]),
                hpv_status=str(row["hpv_status"]),
                icd_10=str(row["icd_10"]),
                icd_o_3_histology=str(row["icd_o_3_histology"]),
                icd_o_3_site=str(row["icd_o_3_site"]),
                lymphatic_invasion=str(row["lymphatic_invasion"]),
                lymphnodes_examined=str(row["lymphnodes_examined"]),
                lymphovascular_invasion_present=str(row["lymphovascular_invasion_present"]),
                menopause_status=str(row["menopause_status"]),
                mononucleotide_and_dinucleotide_marker_panel_analysis_status=str(
                    row["mononucleotide_and_dinucleotide_marker_panel_analysis_status"]),
                mononucleotide_marker_panel_analysis_status=str(row["mononucleotide_marker_panel_analysis_status"]),
                neoplasm_histologic_grade=str(row["neoplasm_histologic_grade"]),
                new_tumor_event_after_initial_treatment=str(row["new_tumor_event_after_initial_treatment"]),
                number_of_lymphnodes_examined=None if "number_of_lymphnodes_examined" not in row or row[
                                                                                                        'number_of_lymphnodes_examined'] is None else int(
                    row["number_of_lymphnodes_examined"]),
                number_of_lymphnodes_positive_by_he=None if "number_of_lymphnodes_positive_by_he" not in row or row[
                                                                                                                    'number_of_lymphnodes_positive_by_he'] is None else int(
                    row["number_of_lymphnodes_positive_by_he"]),
                ParticipantBarcode=str(row["ParticipantBarcode"]),
                pathologic_M=str(row["pathologic_M"]),
                pathologic_N=str(row["pathologic_N"]),
                pathologic_stage=str(row["pathologic_stage"]),
                pathologic_T=str(row["pathologic_T"]),
                person_neoplasm_cancer_status=str(row["person_neoplasm_cancer_status"]),
                pregnancies=str(row["pregnancies"]),
                primary_neoplasm_melanoma_dx=str(row["primary_neoplasm_melanoma_dx"]),
                primary_therapy_outcome_success=str(row["primary_therapy_outcome_success"]),
                prior_dx=str(row["prior_dx"]),
                Project=str(row["Project"]),
                psa_value=None if "psa_value" not in row or row["psa_value"] is None else float(row["psa_value"]),
                race=str(row["race"]),
                residual_tumor=str(row["residual_tumor"]),
                tobacco_smoking_history=str(row["tobacco_smoking_history"]),
                tumor_tissue_site=str(row["tumor_tissue_site"]),
                tumor_type=str(row["tumor_type"]),
                weiss_venous_invasion=str(row["weiss_venous_invasion"]),
                vital_status=str(row["vital_status"]),
                weight=None if "weight" not in row or row["weight"] is None else int(float(row["weight"])),
                year_of_initial_pathologic_diagnosis=str(row["year_of_initial_pathologic_diagnosis"])
            )

            sample_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            sample_cursor.execute(sample_query_str, query_tuple)
            sample_data = []
            for row in sample_cursor.fetchall():
                sample_data.append(row['SampleBarcode'])

            aliquot_cursor = db.cursor(MySQLdb.cursors.DictCursor)
            aliquot_cursor.execute(aliquot_query_str, query_tuple)
            aliquot_data = []
            for row in aliquot_cursor.fetchall():
                aliquot_data.append(row['AliquotBarcode'])

            return PatientDetails(clinical_data=item, samples=sample_data, aliquots=aliquot_data)
        except (IndexError, TypeError), e:
            logger.info("Patient {} not found. Error: {}".format(patient_barcode, e))
            raise endpoints.NotFoundException("Patient {} not found.".format(patient_barcode))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\tpatient query: {} {}\n\tsample query: {} {}\n\taliquot query: {} {}' \
                .format(e, clinical_query_str, query_tuple, sample_query_str, query_tuple,
                        aliquot_query_str, query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving patient, sample, or aliquot data. {}".format(msg))
        finally:
            if clinical_cursor: clinical_cursor.close()
            if sample_cursor: sample_cursor.close()
            if aliquot_cursor: aliquot_cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)