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

import logging
import collections
from datetime import datetime
import endpoints
from protorpc import messages, message_types
from protorpc import remote
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from django.core.signals import request_finished
import django
import MySQLdb
import json
from metadata import MetadataItem
from cohorts.models import Cohort as Django_Cohort, Cohort_Perms, Patients, Samples, Filters
from bq_data_access.cohort_bigquery import BigQueryCohortSupport
from api_helpers import *

logger = logging.getLogger(__name__)

INSTALLED_APP_CLIENT_ID = settings.INSTALLED_APP_CLIENT_ID
CONTROLLED_ACL_GOOGLE_GROUP = settings.ACL_GOOGLE_GROUP
BASE_URL = settings.BASE_URL

DEFAULT_COHORT_NAME = 'Untitled Cohort'

IMPORTANT_FEATURES = [
    'tumor_tissue_site',
    'gender',
    'vital_status',
    'country',
    'Study',
    'age_at_initial_pathologic_diagnosis',
    'TP53',
    'RB1',
    'NF1',
    'APC',
    'CTNNB1',
    'PIK3CA',
    'PTEN',
    'FBXW7',
    'NRAS',
    'ARID1A',
    'CDKN2A',
    'SMAD4',
    'BRAF',
    'NFE2L2',
    'IDH1',
    'PIK3R1',
    'HRAS',
    'EGFR',
    'BAP1',
    'KRAS',
    'DNAseq_data',
    'mirnPlatform',
    'cnvrPlatform',
    'methPlatform',
    'gexpPlatform',
    'rppaPlatform'
]

BUILTIN_ENDPOINTS_PARAMETERS = [
    'alt',
    'fields',
    'enum',
    'enumDescriptions',
    'key',
    'oauth_token',
    'prettyPrint',
    'quotaUser',
    'userIp'
]

MAX_FILTER_VALUE_LENGTH = 496  # max_len of Filter.value is 512, but 507 is too long. 495 is ok.


class ReturnJSON(messages.Message):
    msg = messages.StringField(1)


class FilterDetails(messages.Message):
    name = messages.StringField(1)
    value = messages.StringField(2)


class Cohort(messages.Message):
    id = messages.StringField(1)
    name = messages.StringField(2)
    last_date_saved = messages.StringField(3)
    perm = messages.StringField(4)
    email = messages.StringField(5)
    comments = messages.StringField(6)
    source_type = messages.StringField(7)
    source_notes = messages.StringField(8)
    parent_id = messages.IntegerField(9, repeated=True)
    filters = messages.MessageField(FilterDetails, 10, repeated=True)
    num_patients = messages.StringField(11)
    num_samples = messages.StringField(12)


class CohortsList(messages.Message):
    items = messages.MessageField(Cohort, 1, repeated=True)
    count = messages.IntegerField(2)


class CohortPatientsSamplesList(messages.Message):
    patients = messages.StringField(1, repeated=True)
    patient_count = messages.IntegerField(2)
    samples = messages.StringField(3, repeated=True)
    sample_count = messages.IntegerField(4)
    cohort_id = messages.IntegerField(5)


class PatientDetails(messages.Message):
    clinical_data = messages.MessageField(MetadataItem, 1)
    samples = messages.StringField(2, repeated=True)
    aliquots = messages.StringField(3, repeated=True)


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


class DataFileNameKeyList(messages.Message):
    datafilenamekeys = messages.StringField(1, repeated=True)
    count = messages.IntegerField(2)


class GoogleGenomicsItem(messages.Message):
    SampleBarcode = messages.StringField(1)
    GG_dataset_id = messages.StringField(2)
    GG_readgroupset_id = messages.StringField(3)


class GoogleGenomicsList(messages.Message):
    items = messages.MessageField(GoogleGenomicsItem, 1, repeated=True)
    count = messages.IntegerField(2)


class MetadataRangesItem(messages.Message):
    age_at_initial_pathologic_diagnosis = messages.IntegerField(1, repeated=True)
    age_at_initial_pathologic_diagnosis_lte = messages.IntegerField(2)
    age_at_initial_pathologic_diagnosis_gte = messages.IntegerField(3)

    anatomic_neoplasm_subdivision = messages.StringField(4, repeated=True)

    avg_percent_lymphocyte_infiltration = messages.FloatField(5, repeated=True)
    avg_percent_lymphocyte_infiltration_lte = messages.FloatField(6)
    avg_percent_lymphocyte_infiltration_gte = messages.FloatField(7)

    avg_percent_monocyte_infiltration = messages.FloatField(8, repeated=True)
    avg_percent_monocyte_infiltration_lte = messages.FloatField(9)
    avg_percent_monocyte_infiltration_gte = messages.FloatField(10)

    avg_percent_necrosis = messages.FloatField(11, repeated=True)
    avg_percent_necrosis_lte = messages.FloatField(12)
    avg_percent_necrosis_gte = messages.FloatField(13)

    avg_percent_neutrophil_infiltration = messages.FloatField(14, repeated=True)
    avg_percent_neutrophil_infiltration_lte = messages.FloatField(15)
    avg_percent_neutrophil_infiltration_gte = messages.FloatField(16)

    avg_percent_normal_cells = messages.FloatField(17, repeated=True)
    avg_percent_normal_cells_lte = messages.FloatField(18)
    avg_percent_normal_cells_gte = messages.FloatField(19)

    avg_percent_stromal_cells = messages.FloatField(20, repeated=True)
    avg_percent_stromal_cells_lte = messages.FloatField(21)
    avg_percent_stromal_cells_gte = messages.FloatField(22)

    avg_percent_tumor_cells = messages.FloatField(23, repeated=True)
    avg_percent_tumor_cells_lte = messages.FloatField(24)
    avg_percent_tumor_cells_gte = messages.FloatField(25)

    avg_percent_tumor_nuclei = messages.FloatField(26, repeated=True)
    avg_percent_tumor_nuclei_lte = messages.FloatField(27)
    avg_percent_tumor_nuclei_gte = messages.FloatField(28)

    batch_number = messages.IntegerField(29, repeated=True)
    bcr = messages.StringField(30, repeated=True)
    clinical_M = messages.StringField(31, repeated=True)
    clinical_N = messages.StringField(32, repeated=True)
    clinical_stage = messages.StringField(33, repeated=True)
    clinical_T = messages.StringField(34, repeated=True)
    colorectal_cancer = messages.StringField(35, repeated=True)
    country = messages.StringField(36, repeated=True)

    days_to_birth = messages.IntegerField(37, repeated=True)
    days_to_birth_lte = messages.IntegerField(38)
    days_to_birth_gte = messages.IntegerField(39)

    days_to_collection = messages.IntegerField(40, repeated=True)
    days_to_collection_lte = messages.IntegerField(41)
    days_to_collection_gte = messages.IntegerField(42)

    days_to_death = messages.IntegerField(43, repeated=True)
    days_to_death_lte = messages.IntegerField(44)
    days_to_death_gte = messages.IntegerField(45)

    days_to_initial_pathologic_diagnosis = messages.IntegerField(46, repeated=True)
    days_to_initial_pathologic_diagnosis_lte = messages.IntegerField(47)
    days_to_initial_pathologic_diagnosis_gte = messages.IntegerField(48)

    days_to_last_followup = messages.IntegerField(49, repeated=True)
    days_to_last_followup_lte = messages.IntegerField(50)
    days_to_last_followup_gte = messages.IntegerField(51)

    days_to_submitted_specimen_dx = messages.IntegerField(52, repeated=True)
    days_to_submitted_specimen_dx_lte = messages.IntegerField(53)
    days_to_submitted_specimen_dx_gte = messages.IntegerField(54)

    ethnicity = messages.StringField(55, repeated=True)
    frozen_specimen_anatomic_site = messages.StringField(56, repeated=True)
    gender = messages.StringField(57, repeated=True)

    has_Illumina_DNASeq = messages.StringField(58, repeated=True)
    has_BCGSC_HiSeq_RNASeq = messages.StringField(59, repeated=True)
    has_UNC_HiSeq_RNASeq = messages.StringField(60, repeated=True)
    has_BCGSC_GA_RNASeq = messages.StringField(61, repeated=True)
    has_UNC_GA_RNASeq = messages.StringField(62, repeated=True)
    has_HiSeq_miRnaSeq = messages.StringField(63, repeated=True)
    has_GA_miRNASeq = messages.StringField(64, repeated=True)
    has_RPPA = messages.StringField(65, repeated=True)
    has_SNP6 = messages.StringField(66, repeated=True)
    has_27k = messages.StringField(67, repeated=True)
    has_450k = messages.StringField(68, repeated=True)

    height = messages.IntegerField(69, repeated=True)
    height_lte = messages.IntegerField(70)
    height_gte = messages.IntegerField(71)

    histological_type = messages.StringField(72, repeated=True)
    history_of_colon_polyps = messages.StringField(73, repeated=True)
    history_of_neoadjuvant_treatment = messages.StringField(74, repeated=True)
    history_of_prior_malignancy = messages.StringField(75, repeated=True)
    hpv_calls = messages.StringField(76, repeated=True)
    hpv_status = messages.StringField(77, repeated=True)
    icd_10 = messages.StringField(78, repeated=True)
    icd_o_3_histology = messages.StringField(79, repeated=True)
    icd_o_3_site = messages.StringField(80, repeated=True)
    lymphatic_invasion = messages.StringField(81, repeated=True)
    lymphnodes_examined = messages.StringField(82, repeated=True)
    lymphovascular_invasion_present = messages.StringField(83, repeated=True)

    max_percent_lymphocyte_infiltration = messages.IntegerField(84, repeated=True)
    max_percent_lymphocyte_infiltration_lte = messages.IntegerField(85)
    max_percent_lymphocyte_infiltration_gte = messages.IntegerField(86)

    max_percent_monocyte_infiltration = messages.IntegerField(87, repeated=True)
    max_percent_monocyte_infiltration_lte = messages.IntegerField(88)
    max_percent_monocyte_infiltration_gte = messages.IntegerField(89)

    max_percent_necrosis = messages.IntegerField(90, repeated=True)
    max_percent_necrosis_lte = messages.IntegerField(91)
    max_percent_necrosis_gte = messages.IntegerField(92)

    max_percent_neutrophil_infiltration = messages.IntegerField(93, repeated=True)
    max_percent_neutrophil_infiltration_lte = messages.IntegerField(94)
    max_percent_neutrophil_infiltration_gte = messages.IntegerField(95)

    max_percent_normal_cells = messages.IntegerField(96, repeated=True)
    max_percent_normal_cells_lte = messages.IntegerField(97)
    max_percent_normal_cells_gte = messages.IntegerField(98)

    max_percent_stromal_cells = messages.IntegerField(99, repeated=True)
    max_percent_stromal_cells_lte = messages.IntegerField(100)
    max_percent_stromal_cells_gte = messages.IntegerField(101)

    max_percent_tumor_cells = messages.IntegerField(102, repeated=True)
    max_percent_tumor_cells_lte = messages.IntegerField(103)
    max_percent_tumor_cells_gte = messages.IntegerField(104)

    max_percent_tumor_nuclei = messages.IntegerField(105, repeated=True)
    max_percent_tumor_nuclei_lte = messages.IntegerField(106)
    max_percent_tumor_nuclei_gte = messages.IntegerField(107)

    menopause_status = messages.StringField(108, repeated=True)

    min_percent_lymphocyte_infiltration = messages.IntegerField(109, repeated=True)
    min_percent_lymphocyte_infiltration_lte = messages.IntegerField(110)
    min_percent_lymphocyte_infiltration_gte = messages.IntegerField(111)

    min_percent_monocyte_infiltration = messages.IntegerField(112, repeated=True)
    min_percent_monocyte_infiltration_lte = messages.IntegerField(113)
    min_percent_monocyte_infiltration_gte = messages.IntegerField(114)

    min_percent_necrosis = messages.IntegerField(115, repeated=True)
    min_percent_necrosis_lte = messages.IntegerField(116)
    min_percent_necrosis_gte = messages.IntegerField(117)

    min_percent_neutrophil_infiltration = messages.IntegerField(118, repeated=True)
    min_percent_neutrophil_infiltration_lte = messages.IntegerField(119)
    min_percent_neutrophil_infiltration_gte = messages.IntegerField(120)

    min_percent_normal_cells = messages.IntegerField(121, repeated=True)
    min_percent_normal_cells_lte = messages.IntegerField(122)
    min_percent_normal_cells_gte = messages.IntegerField(123)

    min_percent_stromal_cells = messages.IntegerField(124, repeated=True)
    min_percent_stromal_cells_lte = messages.IntegerField(125)
    min_percent_stromal_cells_gte = messages.IntegerField(126)

    min_percent_tumor_cells = messages.IntegerField(127, repeated=True)
    min_percent_tumor_cells_lte = messages.IntegerField(128)
    min_percent_tumor_cells_gte = messages.IntegerField(129)

    min_percent_tumor_nuclei = messages.IntegerField(130, repeated=True)
    min_percent_tumor_nuclei_lte = messages.IntegerField(131)
    min_percent_tumor_nuclei_gte = messages.IntegerField(132)

    mononucleotide_and_dinucleotide_marker_panel_analysis_status = messages.StringField(133, repeated=True)
    mononucleotide_marker_panel_analysis_status = messages.StringField(134, repeated=True)
    neoplasm_histologic_grade = messages.StringField(135, repeated=True)
    new_tumor_event_after_initial_treatment = messages.StringField(136, repeated=True)

    number_of_lymphnodes_examined = messages.IntegerField(137, repeated=True)
    number_of_lymphnodes_examined_lte = messages.IntegerField(138)
    number_of_lymphnodes_examined_gte = messages.IntegerField(139)

    number_of_lymphnodes_positive_by_he = messages.IntegerField(140, repeated=True)
    number_of_lymphnodes_positive_by_he_lte = messages.IntegerField(141)
    number_of_lymphnodes_positive_by_he_gte = messages.IntegerField(142)

    ParticipantBarcode = messages.StringField(143, repeated=True)
    pathologic_M = messages.StringField(144, repeated=True)
    pathologic_N = messages.StringField(145, repeated=True)
    pathologic_stage = messages.StringField(146, repeated=True)
    pathologic_T = messages.StringField(147, repeated=True)
    person_neoplasm_cancer_status = messages.StringField(148, repeated=True)
    pregnancies = messages.StringField(149, repeated=True)
    primary_neoplasm_melanoma_dx = messages.StringField(150, repeated=True)
    primary_therapy_outcome_success = messages.StringField(151, repeated=True)
    prior_dx = messages.StringField(152, repeated=True)
    Project = messages.StringField(153, repeated=True)

    psa_value = messages.FloatField(154, repeated=True)
    psa_value_lte = messages.FloatField(155)
    psa_value_gte = messages.FloatField(156)

    race = messages.StringField(157, repeated=True)
    residual_tumor = messages.StringField(158, repeated=True)
    SampleBarcode = messages.StringField(159, repeated=True)
    SampleTypeCode = messages.StringField(160, repeated=True)
    Study = messages.StringField(161, repeated=True)
    tobacco_smoking_history = messages.StringField(162, repeated=True)
    tumor_tissue_site = messages.StringField(163, repeated=True)
    tumor_type = messages.StringField(164, repeated=True)
    weiss_venous_invasion = messages.StringField(165, repeated=True)
    vital_status = messages.StringField(166, repeated=True)

    weight = messages.IntegerField(167, repeated=True)
    weight_lte = messages.IntegerField(168)
    weight_gte = messages.IntegerField(169)

    year_of_initial_pathologic_diagnosis = messages.IntegerField(170, repeated=True)
    year_of_initial_pathologic_diagnosis_lte = messages.IntegerField(171)
    year_of_initial_pathologic_diagnosis_gte = messages.IntegerField(172)


def are_there_bad_keys(request):
    '''
    Checks for unrecognized fields in an endpoint request
    :param request: the request object from the endpoint
    :return: boolean indicating True if bad (unrecognized) fields are present in the request
    '''
    unrecognized_param_dict = {
        k: request.get_unrecognized_field_info(k)[0]
        for k in request.all_unrecognized_fields()
        if k not in BUILTIN_ENDPOINTS_PARAMETERS
        }
    return unrecognized_param_dict != {}


def are_there_no_acceptable_keys(request):
    """
    Checks for a lack of recognized fields in an endpoints request. Used in save_cohort and preview_cohort endpoints.
    :param request: the request object from the endpoint
    :return: boolean indicating True if there are no recognized fields in the request.
    """
    param_dict = {
        k.name: request.get_assigned_value(k.name)
        for k in request.all_fields()
        if request.get_assigned_value(k.name)
        }
    return param_dict == {}


def construct_parameter_error_message(request, filter_required):
    err_msg = ''
    sorted_acceptable_keys = sorted([k.name for k in request.all_fields()], key=lambda s: s.lower())
    unrecognized_param_dict = {
        k: request.get_unrecognized_field_info(k)[0]
        for k in request.all_unrecognized_fields()
        if k not in BUILTIN_ENDPOINTS_PARAMETERS
        }
    if unrecognized_param_dict:
        bad_key_str = "'" + "', '".join(unrecognized_param_dict.keys()) + "'"
        err_msg += "The following filters were not recognized: {}. ".format(bad_key_str)
    if filter_required:
        err_msg += "You must specify at least one of the following " \
                   "case-sensitive filters: {}".format(sorted_acceptable_keys)
    else:
        err_msg += "Acceptable filters are: {}".format(sorted_acceptable_keys)

    return err_msg


def get_list_of_split_values_for_filter_model(large_value_list):
    '''
    :rtype: list
    :param large_value_list: protorpc.messages.FieldList
    :return: list of smaller protorpc.messages.FieldLists
    '''

    return_list = []

    # if length_of_list is larger than 512 characters,
    # the Filter model will not be able to be saved
    # with this as the value field
    length_of_list = len('"' + '", "'.join(large_value_list) + '"')
    while length_of_list > MAX_FILTER_VALUE_LENGTH:
        new_smaller_list = []
        length_of_smaller_list = len('"' + '", "'.join(new_smaller_list) + '"')
        while length_of_smaller_list < MAX_FILTER_VALUE_LENGTH:
            try:
                new_smaller_list.append(large_value_list.pop())
            except IndexError:
                break
            length_of_smaller_list = len('"' + '", "'.join(new_smaller_list) + '"')
        large_value_list.append(new_smaller_list.pop())
        return_list.append(new_smaller_list)
        length_of_list = len('"' + '", "'.join(large_value_list) + '"')

    if len(large_value_list):
        return_list.append(large_value_list)

    return return_list


Cohort_Endpoints = endpoints.api(name='cohort_api', version='v1',
                                 description="Get information about cohorts, patients, and samples. Create and delete cohorts.",
                                 allowed_client_ids=[INSTALLED_APP_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])


@Cohort_Endpoints.api_class(resource_name='cohort_endpoints')
class Cohort_Endpoints_API(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(token=messages.StringField(1), cohort_id=messages.IntegerField(2))

    @endpoints.method(GET_RESOURCE, CohortsList,
                      path='cohorts_list', http_method='GET', name='cohorts.list')
    def cohorts_list(self, request):
        '''
        Returns information about cohorts a user has either READER or OWNER permission on.
        Authentication is required. Optionally takes a cohort id as a parameter to
        only list information about one cohort.
        '''
        user_email = None
        cursor = None
        filter_cursor = None
        parent_cursor = None
        db = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        # users have the option of pasting the access token in the query string
        # or in the 'token' field in the api explorer
        # but this is not required
        access_token = request.get_assigned_value('token')
        if access_token:
            user_email = get_user_email_from_token(access_token)

        cohort_id = request.get_assigned_value('cohort_id')

        if user_email:
            django.setup()
            try:
                user_id = Django_User.objects.get(email=user_email).id
            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)

            query_dict = {'cohorts_cohort_perms.user_id': user_id, 'cohorts_cohort.active': unicode('1')}

            if cohort_id:
                query_dict['cohorts_cohort.id'] = cohort_id

            query_str = 'select cohorts_cohort.id, ' \
                        'cohorts_cohort.name, ' \
                        'cohorts_cohort.last_date_saved, ' \
                        'cohorts_cohort_perms.perm, ' \
                        'auth_user.email, ' \
                        'cohorts_cohort_comments.content as comments, ' \
                        'cohorts_source.type as source_type, ' \
                        'cohorts_source.notes as source_notes ' \
                        'from cohorts_cohort_perms ' \
                        'join cohorts_cohort ' \
                        'on cohorts_cohort.id=cohorts_cohort_perms.cohort_id ' \
                        'join auth_user ' \
                        'on auth_user.id=cohorts_cohort_perms.user_id ' \
                        'left join cohorts_cohort_comments ' \
                        'on cohorts_cohort_comments.user_id=cohorts_cohort_perms.user_id ' \
                        'and cohorts_cohort_comments.cohort_id=cohorts_cohort.id ' \
                        'left join cohorts_source ' \
                        'on cohorts_source.cohort_id=cohorts_cohort_perms.cohort_id '



            query_tuple = ()
            if query_dict:
                query_str += ' where ' + '=%s and '.join(key for key in query_dict.keys()) + '=%s '
                query_tuple = tuple(value for value in query_dict.values())

            query_str += 'group by  ' \
                         'cohorts_cohort.id,  ' \
                         'cohorts_cohort.name,  ' \
                         'cohorts_cohort.last_date_saved,  ' \
                         'cohorts_cohort_perms.perm,  ' \
                         'auth_user.email,  ' \
                         'comments,  ' \
                         'source_type,  ' \
                         'source_notes '

            print query_str
            print query_tuple

            filter_query_str = ''
            parent_id_query_str = ''
            row = None

            try:
                db = sql_connection()
                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query_str, query_tuple)
                data = []

                for row in cursor.fetchall():
                    filter_query_str = 'SELECT name, value ' \
                                       'FROM cohorts_filters ' \
                                       'WHERE cohorts_filters.resulting_cohort_id=%s'

                    filter_cursor = db.cursor(MySQLdb.cursors.DictCursor)
                    filter_cursor.execute(filter_query_str, (str(row['id']),))
                    filter_data = []
                    for filter_row in filter_cursor.fetchall():
                        filter_data.append(FilterDetails(
                            name=str(filter_row['name']),
                            value=str(filter_row['value'])
                        ))

                    # getting the parent_id is a separate query since a single cohort
                    # may have multiple parent cohorts
                    parent_id_query_str = 'SELECT parent_id ' \
                                          'FROM cohorts_source ' \
                                          'WHERE cohort_id=%s'

                    parent_cursor = db.cursor(MySQLdb.cursors.DictCursor)
                    parent_cursor.execute(parent_id_query_str, (str(row['id']),))
                    parent_id_data = []
                    for parent_row in parent_cursor.fetchall():
                        if row.get('parent_id') is not None:
                            parent_id_data.append(int(parent_row['parent_id']))

                    data.append(Cohort(
                        id=str(row['id']),
                        name=str(row['name']),
                        last_date_saved=str(row['last_date_saved']),
                        perm=str(row['perm']),
                        email=str(row['email']),
                        comments=str(row['comments']),
                        source_type=None if row['source_type'] is None else str(row['source_type']),
                        source_notes=None if row['source_notes'] is None else str(row['source_notes']),
                        parent_id=parent_id_data,
                        filters=filter_data
                    ))

                if len(data) == 0:
                    optional_message = " matching cohort id " + str(cohort_id) if cohort_id is not None else ""
                    raise endpoints.NotFoundException("{} has no active cohorts{}."
                                                      .format(user_email, optional_message))
                return CohortsList(items=data, count=len(data))
            except (IndexError, TypeError) as e:
                raise endpoints.NotFoundException(
                    "User {}'s cohorts not found. {}: {}".format(user_email, type(e), e))
            except MySQLdb.ProgrammingError as e:
                msg = '{}:\n\tcohort query: {} {}\n\tfilter query: {} {}\n\tparent id query: {} {}' \
                    .format(e, query_str, query_tuple, filter_query_str, str(row['id']), parent_id_query_str,
                            str(row['id']))
                logger.warn(msg)
                raise endpoints.BadRequestException("Error retrieving cohorts or filters. {}".format(msg))
            finally:
                if cursor: cursor.close()
                if filter_cursor: filter_cursor.close()
                if parent_cursor: parent_cursor.close()
                if db and db.open: db.close()
                request_finished.send(self)
        else:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

    GET_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True),
                                               token=messages.StringField(2))

    @endpoints.method(GET_RESOURCE, CohortPatientsSamplesList,
                      path='cohort_patients_samples_list', http_method='GET',
                      name='cohorts.cohort_patients_samples_list')
    def cohort_patients_samples_list(self, request):
        """
        Takes a cohort id as a required parameter and returns information about the participants
        and samples in a particular cohort. Authentication is required.
        User must have either READER or OWNER permissions on the cohort.
        """

        db = None
        cursor = None
        user_email = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        # users have the option of pasting the access token in the query string
        # or in the 'token' field in the api explorer
        # but this is not required
        access_token = request.get_assigned_value('token')
        if access_token:
            user_email = get_user_email_from_token(access_token)

        cohort_id = request.get_assigned_value('cohort_id')

        if user_email:
            django.setup()
            try:
                user_id = Django_User.objects.get(email=user_email).id
            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                request_finished.send(self)
                raise endpoints.UnauthorizedException(
                    "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

            cohort_perms_query = "select count(*) from cohorts_cohort_perms where user_id=%s and cohort_id=%s"
            cohort_perms_tuple = (user_id, cohort_id)
            cohort_query = "select count(*) from cohorts_cohort where id=%s and active=%s"
            cohort_tuple = (cohort_id, unicode('0'))

            try:
                db = sql_connection()
                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(cohort_perms_query, cohort_perms_tuple)
                result = cursor.fetchone()
                if int(result['count(*)']) == 0:
                    error_message = "{} does not have owner or reader permissions on cohort {}.".format(user_email,
                                                                                                        cohort_id)
                    request_finished.send(self)
                    raise endpoints.ForbiddenException(error_message)

                cursor.execute(cohort_query, cohort_tuple)
                result = cursor.fetchone()
                if int(result['count(*)']) > 0:
                    error_message = "Cohort {} was deleted.".format(cohort_id)
                    request_finished.send(self)
                    raise endpoints.NotFoundException(error_message)

            except (IndexError, TypeError) as e:
                logger.warn(e)
                raise endpoints.NotFoundException("Cohort {} not found.".format(cohort_id))
            except MySQLdb.ProgrammingError as e:
                msg = '{}:\n\tcohort permissions query: {} {}\n\tcohort query: {} {}' \
                    .format(e, cohort_perms_query, cohort_perms_tuple, cohort_query, cohort_tuple)
                logger.warn(msg)
                raise endpoints.BadRequestException("Error retrieving cohorts or cohort permissions. {}".format(msg))
            finally:
                if cursor: cursor.close()
                if db and db.open: db.close()
                request_finished.send(self)

            patient_query_str = 'select cohorts_patients.patient_id ' \
                                'from cohorts_patients ' \
                                'inner join cohorts_cohort_perms ' \
                                'on cohorts_cohort_perms.cohort_id=cohorts_patients.cohort_id ' \
                                'inner join cohorts_cohort ' \
                                'on cohorts_patients.cohort_id=cohorts_cohort.id ' \
                                'where cohorts_patients.cohort_id=%s ' \
                                'and cohorts_cohort_perms.user_id=%s ' \
                                'and cohorts_cohort.active=%s ' \
                                'group by cohorts_patients.patient_id '

            patient_query_tuple = (cohort_id, user_id, unicode('1'))

            sample_query_str = 'select cohorts_samples.sample_id ' \
                               'from cohorts_samples ' \
                               'inner join cohorts_cohort_perms ' \
                               'on cohorts_cohort_perms.cohort_id=cohorts_samples.cohort_id ' \
                               'inner join cohorts_cohort ' \
                               'on cohorts_samples.cohort_id=cohorts_cohort.id ' \
                               'where cohorts_samples.cohort_id=%s ' \
                               'and cohorts_cohort_perms.user_id=%s ' \
                               'and cohorts_cohort.active=%s ' \
                               'group by cohorts_samples.sample_id '

            sample_query_tuple = (cohort_id, user_id, unicode('1'))

            try:
                db = sql_connection()

                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(patient_query_str, patient_query_tuple)
                patient_data = []
                for row in cursor.fetchall():
                    patient_data.append(row['patient_id'])

                cursor.execute(sample_query_str, sample_query_tuple)
                sample_data = []
                for row in cursor.fetchall():
                    sample_data.append(row['sample_id'])

                return CohortPatientsSamplesList(patients=patient_data,
                                                 patient_count=len(patient_data),
                                                 samples=sample_data,
                                                 sample_count=len(sample_data),
                                                 cohort_id=int(cohort_id))
            except (IndexError, TypeError) as e:
                logger.warn(e)
                raise endpoints.NotFoundException("Cohort {} not found.".format(cohort_id))
            except MySQLdb.ProgrammingError as e:
                msg = '{}:\n\tpatient query: {} {}\n\tsample query: {} {}' \
                    .format(e, patient_query_str, patient_query_tuple, sample_query_str, sample_query_tuple)
                logger.warn(msg)
                raise endpoints.BadRequestException("Error retrieving patients or samples. {}".format(msg))
            finally:
                if cursor: cursor.close()
                if db and db.open: db.close()
                request_finished.send(self)

        else:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

    GET_RESOURCE = endpoints.ResourceContainer(patient_barcode=messages.StringField(1, required=True))

    @endpoints.method(GET_RESOURCE, PatientDetails,
                      path='patient_details', http_method='GET', name='cohorts.patient_details')
    def patient_details(self, request):
        """
        Returns information about a specific participant,
        including a list of samples and aliquots derived from this patient.
        Takes a participant barcode (of length 12, *eg* TCGA-B9-7268) as a required parameter.
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

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True),
                                               platform=messages.StringField(2),
                                               pipeline=messages.StringField(3))

    @endpoints.method(GET_RESOURCE, SampleDetails,
                      path='sample_details', http_method='GET', name='cohorts.sample_details')
    def sample_details(self, request):
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

    GET_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True),
                                               limit=messages.IntegerField(2),
                                               platform=messages.StringField(3),
                                               pipeline=messages.StringField(4),
                                               token=messages.StringField(5))

    @endpoints.method(GET_RESOURCE, DataFileNameKeyList,
                      path='datafilenamekey_list_from_cohort', http_method='GET',
                      name='cohorts.datafilenamekey_list_from_cohort')
    def datafilenamekey_list_from_cohort(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        user_email = None
        cursor = None
        db = None

        limit = request.get_assigned_value('limit')
        platform = request.get_assigned_value('platform')
        pipeline = request.get_assigned_value('pipeline')
        cohort_id = request.get_assigned_value('cohort_id')

        if are_there_bad_keys(request):
            err_msg = construct_parameter_error_message(request, False)
            raise endpoints.BadRequestException(err_msg)

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        # users have the option of pasting the access token in the query string
        # or in the 'token' field in the api explorer
        # but this is not required
        access_token = request.get_assigned_value('token')
        if access_token:
            user_email = get_user_email_from_token(access_token)

        if user_email:
            django.setup()

            query_str = 'SELECT DataFileNameKey, SecurityProtocol, Repository ' \
                        'FROM metadata_data '

            try:
                user_id = Django_User.objects.get(email=user_email).id
                django_cohort = Django_Cohort.objects.get(id=cohort_id)
                cohort_perm = Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user_id)
            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                err_msg = "Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e)
                if 'Cohort_Perms' in e.message:
                    err_msg = "User {} does not have permissions on cohort {}. Error: {}" \
                        .format(user_email, cohort_id, e)
                request_finished.send(self)
                raise endpoints.UnauthorizedException(err_msg)

            query_str += 'JOIN cohorts_samples ON metadata_data.SampleBarcode=cohorts_samples.sample_id ' \
                         'WHERE cohorts_samples.cohort_id=%s ' \
                         'AND DataFileNameKey != "" AND DataFileNameKey is not null '
            query_tuple = (cohort_id,)

            if platform:
                query_str += ' and metadata_data.Platform=%s '
                query_tuple += (platform,)

            if pipeline:
                query_str += ' and metadata_data.Pipeline=%s '
                query_tuple += (pipeline,)

            query_str += ' GROUP BY DataFileNameKey, SecurityProtocol, Repository '
            if limit is None:
                query_str += ' LIMIT 10000'
            else:
                query_str += ' LIMIT %s'
                query_tuple += (limit,)

            try:
                db = sql_connection()
                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query_str, query_tuple)

                datafilenamekeys = []
                bad_repo_count = 0
                bad_repo_set = set()
                for row in cursor.fetchall():
                    if not row.get('DataFileNameKey'):
                        continue
                    if 'controlled' not in str(row['SecurityProtocol']).lower():
                        datafilenamekeys.append(
                            "gs://{}{}".format(settings.OPEN_DATA_BUCKET, row.get('DataFileNameKey')))
                    else:  # not filtering on dbGaP_authorized
                        bucket_name = ''
                        if row['Repository'].lower() == 'dcc':
                            bucket_name = settings.DCC_CONTROLLED_DATA_BUCKET
                        elif row['Repository'].lower() == 'cghub':
                            bucket_name = settings.CGHUB_CONTROLLED_DATA_BUCKET
                        else:  # shouldn't ever happen
                            bad_repo_count += 1
                            bad_repo_set.add(row['Repository'])
                            continue
                        datafilenamekeys.append("gs://{}{}".format(bucket_name, row.get('DataFileNameKey')))
                if bad_repo_count > 0:
                    logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                                .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))
                return DataFileNameKeyList(datafilenamekeys=datafilenamekeys, count=len(datafilenamekeys))

            except (IndexError, TypeError), e:
                logger.warn(e)
                raise endpoints.NotFoundException("File paths for cohort {} not found.".format(cohort_id))
            except MySQLdb.ProgrammingError as e:
                msg = '{}:\n\t query: {} {}'.format(e, query_str, query_tuple)
                logger.warn(msg)
                raise endpoints.BadRequestException("Error retrieving file paths. {}".format(msg))
            finally:
                if cursor: cursor.close()
                if db and db.open: db.close()
                request_finished.send(self)

        else:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True),
                                               platform=messages.StringField(2),
                                               pipeline=messages.StringField(3))

    @endpoints.method(GET_RESOURCE, DataFileNameKeyList,
                      path='datafilenamekey_list_from_sample', http_method='GET',
                      name='cohorts.datafilenamekey_list_from_sample')
    def datafilenamekey_list_from_sample(self, request):
        """
        Takes a sample barcode as a required parameter and
        returns cloud storage paths to files associated with that sample.
        """
        cursor = None
        db = None

        sample_barcode = request.get_assigned_value('sample_barcode')
        platform = request.get_assigned_value('platform')
        pipeline = request.get_assigned_value('pipeline')

        if are_there_bad_keys(request):
            err_msg = construct_parameter_error_message(request, False)
            raise endpoints.BadRequestException(err_msg)

        query_str = 'SELECT DataFileNameKey, SecurityProtocol, Repository ' \
                    'FROM metadata_data WHERE SampleBarcode=%s '

        query_tuple = (sample_barcode,)

        if platform:
            query_str += ' and Platform=%s '
            query_tuple += (platform,)

        if pipeline:
            query_str += ' and Pipeline=%s '
            query_tuple += (pipeline,)

        query_str += ' GROUP BY DataFileNameKey, SecurityProtocol, Repository'

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)

            datafilenamekeys = []
            bad_repo_count = 0
            bad_repo_set = set()
            for row in cursor.fetchall():
                if not row.get('DataFileNameKey'):
                    continue
                if 'controlled' not in str(row['SecurityProtocol']).lower():
                    datafilenamekeys.append("gs://{}{}".format(settings.OPEN_DATA_BUCKET, row.get('DataFileNameKey')))
                else:  # not filtering on dbGaP_authorized
                    bucket_name = ''
                    if row['Repository'].lower() == 'dcc':
                        bucket_name = settings.DCC_CONTROLLED_DATA_BUCKET
                    elif row['Repository'].lower() == 'cghub':
                        bucket_name = settings.CGHUB_CONTROLLED_DATA_BUCKET
                    else:  # shouldn't ever happen
                        bad_repo_count += 0
                        bad_repo_set.add(row['Repository'])
                        continue
                    datafilenamekeys.append("gs://{}{}".format(bucket_name, row.get('DataFileNameKey')))
            if bad_repo_count > 0:
                logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                            .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))
            return DataFileNameKeyList(datafilenamekeys=datafilenamekeys, count=len(datafilenamekeys))

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException("File paths for sample {} not found.".format(sample_barcode))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\t query: {} {}'.format(e, query_str, query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving file paths. {}".format(msg))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()

    POST_RESOURCE = endpoints.ResourceContainer(MetadataRangesItem,
                                                name=messages.StringField(2, required=True),
                                                token=messages.StringField(3))

    @endpoints.method(POST_RESOURCE, Cohort,
                      path='save_cohort', http_method='POST', name='cohorts.save_cohort')
    def save_cohort(self, request):
        """
        Creates and saves a cohort. Takes a JSON object in the request body to use as the cohort's filters.
        Authentication is required.
        Returns information about the saved cohort, including the number of patients and samples in that cohort.
        """
        user_email = None
        patient_cursor = None
        sample_cursor = None
        db = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        # users have the option of pasting the access token in the query string
        # or in the 'token' field in the api explorer
        # but this is not required
        access_token = request.get_assigned_value('token')
        if access_token:
            user_email = get_user_email_from_token(access_token)

        if user_email:
            django.setup()
            try:
                django_user = Django_User.objects.get(email=user_email)
                user_id = django_user.id
            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                request_finished.send(self)
                raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)

            if are_there_bad_keys(request) or are_there_no_acceptable_keys(request):
                err_msg = construct_parameter_error_message(request, True)
                request_finished.send(self)
                raise endpoints.BadRequestException(err_msg)

            query_dict = {
                k.name: request.get_assigned_value(k.name)
                for k in request.all_fields()
                if request.get_assigned_value(k.name) and k.name is not 'name' and k.name is not 'token'
                and not k.name.endswith('_gte')
                and not k.name.endswith('_lte')
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
                if isinstance(value_list, collections.Iterable) and "None" in value_list:
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
                raise endpoints.NotFoundException("Error retrieving samples or patients")
            except MySQLdb.ProgrammingError as e:
                msg = '{}:\n\tpatient query: {} {}\n\tsample query: {} {}' \
                    .format(e, patient_query_str, value_tuple, sample_query_str, value_tuple)
                logger.warn(msg)
                raise endpoints.BadRequestException("Error saving cohort. {}".format(msg))
            finally:
                if patient_cursor: patient_cursor.close()
                if sample_cursor: sample_cursor.close()
                if db and db.open: db.close()
                request_finished.send(self)

            cohort_name = request.get_assigned_value('name')

            # 1. create new cohorts_cohort with name, active=True, last_date_saved=now
            created_cohort = Django_Cohort.objects.create(name=cohort_name, active=True,
                                                          last_date_saved=datetime.utcnow())
            created_cohort.save()

            # 2. insert patients into cohort_patients
            patient_barcodes = list(set(patient_barcodes))
            patient_list = [Patients(cohort=created_cohort, patient_id=patient_code) for patient_code in
                            patient_barcodes]
            Patients.objects.bulk_create(patient_list)

            # 3. insert samples into cohort_samples
            sample_barcodes = list(set(sample_barcodes))
            sample_list = [Samples(cohort=created_cohort, sample_id=sample_code) for sample_code in sample_barcodes]
            Samples.objects.bulk_create(sample_list)

            # 4. Set permission for user to be owner
            perm = Cohort_Perms(cohort=created_cohort, user=django_user, perm=Cohort_Perms.OWNER)
            perm.save()

            # 5. Create filters applied
            filter_data = []
            for key, value_list in query_dict.items():
                for val in value_list:
                    filter_data.append(FilterDetails(name=key, value=str(val)))
                    Filters.objects.create(resulting_cohort=created_cohort, name=key, value=val).save()

            for key, val in [(k + '_lte', v) for k, v in lte_query_dict.items()] + [(k + '_gte', v) for k, v in gte_query_dict.items()]:
                filter_data.append(FilterDetails(name=key, value=str(val)))
                Filters.objects.create(resulting_cohort=created_cohort, name=key, value=val).save()

            # 6. Store cohort to BigQuery
            project_id = settings.BQ_PROJECT_ID
            cohort_settings = settings.GET_BQ_COHORT_SETTINGS()
            bcs = BigQueryCohortSupport(project_id, cohort_settings.dataset_id, cohort_settings.table_id)
            bcs.add_cohort_with_sample_barcodes(created_cohort.id, sample_barcodes)

            request_finished.send(self)
            return Cohort(id=str(created_cohort.id),
                          name=cohort_name,
                          last_date_saved=str(datetime.utcnow()),
                          num_patients=str(len(patient_barcodes)),
                          num_samples=str(len(sample_barcodes))
                          )

        else:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

    DELETE_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True),
                                                  token=messages.StringField(2))

    @endpoints.method(DELETE_RESOURCE, ReturnJSON,
                      path='delete_cohort', http_method='POST', name='cohorts.delete')
    def delete_cohort(self, request):
        """
        Deletes a cohort. User must have owner permissions on the cohort.
        """
        user_email = None
        return_message = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        # users have the option of pasting the access token in the query string
        # or in the 'token' field in the api explorer
        # but this is not required
        access_token = request.get_assigned_value('token')
        if access_token:
            user_email = get_user_email_from_token(access_token)

        cohort_id = request.get_assigned_value('cohort_id')

        if user_email:
            django.setup()
            try:
                django_user = Django_User.objects.get(email=user_email)
                user_id = django_user.id
            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                request_finished.send(self)
                raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)
            try:
                cohort_to_deactivate = Django_Cohort.objects.get(id=cohort_id)
                if cohort_to_deactivate.active is True:
                    cohort_perm = Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user_id)
                    if cohort_perm.perm == 'OWNER':
                        cohort_to_deactivate.active = False
                        cohort_to_deactivate.save()
                        return_message = 'Cohort %d successfully deactivated.' % cohort_id
                    else:
                        return_message = 'You do not have owner permission on cohort %d.' % cohort_id
                else:
                    return_message = "Cohort %d was already deactivated." % cohort_id

            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                raise endpoints.NotFoundException(
                    "Either cohort %d does not have an entry in the database "
                    "or you do not have owner or reader permissions on this cohort." % cohort_id)
            finally:
                request_finished.send(self)
        else:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

        return ReturnJSON(msg=return_message)

    POST_RESOURCE = endpoints.ResourceContainer(MetadataRangesItem)

    @endpoints.method(POST_RESOURCE, CohortPatientsSamplesList,
                      path='preview_cohort', http_method='POST', name='cohorts.preview_cohort')
    def preview_cohort(self, request):
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

        if are_there_bad_keys(request) or are_there_no_acceptable_keys(request):
            err_msg = construct_parameter_error_message(request, True)
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

        return CohortPatientsSamplesList(patients=patient_barcodes,
                                         patient_count=len(patient_barcodes),
                                         samples=sample_barcodes,
                                         sample_count=len(sample_barcodes))

    GET_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True),
                                               token=messages.StringField(2))

    @endpoints.method(GET_RESOURCE, GoogleGenomicsList,
                      path='google_genomics_from_cohort', http_method='GET', name='cohorts.google_genomics_from_cohort')
    def google_genomics_from_cohort(self, request):
        """
        Returns a list of Google Genomics dataset and readgroupset ids associated with
        all the samples in a specified cohort.
        Authentication is required. User must have either READER or OWNER permissions on the cohort.
        """
        cursor = None
        db = None
        user_email = None
        cohort_id = request.get_assigned_value('cohort_id')

        if are_there_bad_keys(request):
            err_msg = construct_parameter_error_message(request, False)
            raise endpoints.BadRequestException(err_msg)

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        # users have the option of pasting the access token in the query string
        # or in the 'token' field in the api explorer
        # but this is not required
        access_token = request.get_assigned_value('token')
        if access_token:
            user_email = get_user_email_from_token(access_token)

        if user_email:
            django.setup()
            try:
                user_id = Django_User.objects.get(email=user_email).id
                django_cohort = Django_Cohort.objects.get(id=cohort_id)
                cohort_perm = Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user_id)
            except (ObjectDoesNotExist, MultipleObjectsReturned), e:
                logger.warn(e)
                err_msg = "Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e)
                if 'Cohort_Perms' in e.message:
                    err_msg = "User {} does not have permissions on cohort {}. Error: {}" \
                        .format(user_email, cohort_id, e)
                request_finished.send(self)
                raise endpoints.UnauthorizedException(err_msg)

            query_str = 'SELECT SampleBarcode, GG_dataset_id, GG_readgroupset_id ' \
                        'FROM metadata_data ' \
                        'JOIN cohorts_samples ON metadata_data.SampleBarcode=cohorts_samples.sample_id ' \
                        'WHERE cohorts_samples.cohort_id=%s ' \
                        'AND GG_dataset_id !="" AND GG_readgroupset_id !="" ' \
                        'GROUP BY SampleBarcode, GG_dataset_id, GG_readgroupset_id;'

            query_tuple = (cohort_id,)
            try:
                db = sql_connection()
                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query_str, query_tuple)

                google_genomics_items = []
                for row in cursor.fetchall():
                    google_genomics_items.append(
                        GoogleGenomicsItem(
                            SampleBarcode=row['SampleBarcode'],
                            GG_dataset_id=row['GG_dataset_id'],
                            GG_readgroupset_id=row['GG_readgroupset_id']
                        )
                    )

                return GoogleGenomicsList(items=google_genomics_items, count=len(google_genomics_items))

            except (IndexError, TypeError), e:
                logger.warn(e)
                raise endpoints.NotFoundException(
                    "Google Genomics dataset and readgroupset id's for cohort {} not found."
                        .format(cohort_id))
            except MySQLdb.ProgrammingError as e:
                msg = '{}:\n\tquery: {} {}' \
                    .format(e, query_str, query_tuple)
                logger.warn(msg)
                raise endpoints.BadRequestException("Error retrieving genomics data for cohort. {}".format(msg))
            finally:
                if cursor: cursor.close()
                if db and db.open: db.close()
                request_finished.send(self)
        else:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True))

    @endpoints.method(GET_RESOURCE, GoogleGenomicsList,
                      path='google_genomics_from_sample', http_method='GET',
                      name='cohorts.google_genomics_from_sample')
    def google_genomics_from_sample(self, request):
        """
        Takes a sample barcode as a required parameter and returns the Google Genomics dataset id
        and readgroupset id associated with the sample, if any.
        """
        # print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
        cursor = None
        db = None
        sample_barcode = request.get_assigned_value('sample_barcode')

        if are_there_bad_keys(request):
            err_msg = construct_parameter_error_message(request, False)
            raise endpoints.BadRequestException(err_msg)

        query_str = 'SELECT SampleBarcode, GG_dataset_id, GG_readgroupset_id ' \
                    'FROM metadata_data ' \
                    'WHERE SampleBarcode=%s ' \
                    'AND GG_dataset_id !="" AND GG_readgroupset_id !="" ' \
                    'GROUP BY SampleBarcode, GG_dataset_id, GG_readgroupset_id;'

        query_tuple = (sample_barcode,)
        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)

            google_genomics_items = []
            for row in cursor.fetchall():
                google_genomics_items.append(
                    GoogleGenomicsItem(
                        SampleBarcode=row['SampleBarcode'],
                        GG_dataset_id=row['GG_dataset_id'],
                        GG_readgroupset_id=row['GG_readgroupset_id']
                    )
                )

            return GoogleGenomicsList(items=google_genomics_items, count=len(google_genomics_items))

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException(
                "Google Genomics dataset and readgroupset id's for sample {} not found."
                    .format(sample_barcode))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\tquery: {} {}' \
                .format(e, query_str, query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving genomics data for sample. {}".format(msg))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
