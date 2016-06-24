import endpoints
from django.conf import settings
from protorpc import messages

INSTALLED_APP_CLIENT_ID = settings.INSTALLED_APP_CLIENT_ID
CONTROLLED_ACL_GOOGLE_GROUP = settings.ACL_GOOGLE_GROUP

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

ISB_CGC_Endpoints = endpoints.api(name='isb_cgc_api', version='v2',
                                  description="Get information about cohorts, patients, and samples. Create and delete cohorts.",
                                  allowed_client_ids=[INSTALLED_APP_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID,
                                                      settings.WEB_CLIENT_ID],
                                  documentation='http://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/Programmatic-API.html',
                                  title="ISB-CGC API")


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

    max_percent_lymphocyte_infiltration = messages.FloatField(84, repeated=True)
    max_percent_lymphocyte_infiltration_lte = messages.FloatField(85)
    max_percent_lymphocyte_infiltration_gte = messages.FloatField(86)

    max_percent_monocyte_infiltration = messages.FloatField(87, repeated=True)
    max_percent_monocyte_infiltration_lte = messages.FloatField(88)
    max_percent_monocyte_infiltration_gte = messages.FloatField(89)

    max_percent_necrosis = messages.FloatField(90, repeated=True)
    max_percent_necrosis_lte = messages.FloatField(91)
    max_percent_necrosis_gte = messages.FloatField(92)

    max_percent_neutrophil_infiltration = messages.FloatField(93, repeated=True)
    max_percent_neutrophil_infiltration_lte = messages.FloatField(94)
    max_percent_neutrophil_infiltration_gte = messages.FloatField(95)

    max_percent_normal_cells = messages.FloatField(96, repeated=True)
    max_percent_normal_cells_lte = messages.FloatField(97)
    max_percent_normal_cells_gte = messages.FloatField(98)

    max_percent_stromal_cells = messages.FloatField(99, repeated=True)
    max_percent_stromal_cells_lte = messages.FloatField(100)
    max_percent_stromal_cells_gte = messages.FloatField(101)

    max_percent_tumor_cells = messages.FloatField(102, repeated=True)
    max_percent_tumor_cells_lte = messages.FloatField(103)
    max_percent_tumor_cells_gte = messages.FloatField(104)

    max_percent_tumor_nuclei = messages.FloatField(105, repeated=True)
    max_percent_tumor_nuclei_lte = messages.FloatField(106)
    max_percent_tumor_nuclei_gte = messages.FloatField(107)

    menopause_status = messages.StringField(108, repeated=True)

    min_percent_lymphocyte_infiltration = messages.FloatField(109, repeated=True)
    min_percent_lymphocyte_infiltration_lte = messages.FloatField(110)
    min_percent_lymphocyte_infiltration_gte = messages.FloatField(111)

    min_percent_monocyte_infiltration = messages.FloatField(112, repeated=True)
    min_percent_monocyte_infiltration_lte = messages.FloatField(113)
    min_percent_monocyte_infiltration_gte = messages.FloatField(114)

    min_percent_necrosis = messages.FloatField(115, repeated=True)
    min_percent_necrosis_lte = messages.FloatField(116)
    min_percent_necrosis_gte = messages.FloatField(117)

    min_percent_neutrophil_infiltration = messages.FloatField(118, repeated=True)
    min_percent_neutrophil_infiltration_lte = messages.FloatField(119)
    min_percent_neutrophil_infiltration_gte = messages.FloatField(120)

    min_percent_normal_cells = messages.FloatField(121, repeated=True)
    min_percent_normal_cells_lte = messages.FloatField(122)
    min_percent_normal_cells_gte = messages.FloatField(123)

    min_percent_stromal_cells = messages.FloatField(124, repeated=True)
    min_percent_stromal_cells_lte = messages.FloatField(125)
    min_percent_stromal_cells_gte = messages.FloatField(126)

    min_percent_tumor_cells = messages.FloatField(127, repeated=True)
    min_percent_tumor_cells_lte = messages.FloatField(128)
    min_percent_tumor_cells_gte = messages.FloatField(129)

    min_percent_tumor_nuclei = messages.FloatField(130, repeated=True)
    min_percent_tumor_nuclei_lte = messages.FloatField(131)
    min_percent_tumor_nuclei_gte = messages.FloatField(132)

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


class MetadataItem(messages.Message):
    adenocarcinoma_invasion                                         = messages.StringField(1)
    age_at_initial_pathologic_diagnosis                             = messages.IntegerField(2)
    anatomic_neoplasm_subdivision                                   = messages.StringField(3)
    avg_percent_lymphocyte_infiltration                             = messages.FloatField(4)
    avg_percent_monocyte_infiltration                               = messages.FloatField(5)
    avg_percent_necrosis                                            = messages.FloatField(6)
    avg_percent_neutrophil_infiltration                             = messages.FloatField(7)
    avg_percent_normal_cells                                        = messages.FloatField(8)
    avg_percent_stromal_cells                                       = messages.FloatField(9)
    avg_percent_tumor_cells                                         = messages.FloatField(10)
    avg_percent_tumor_nuclei                                        = messages.FloatField(11)
    batch_number                                                    = messages.IntegerField(12)
    bcr                                                             = messages.StringField(13)
    clinical_M                                                      = messages.StringField(14)
    clinical_N                                                      = messages.StringField(15)
    clinical_stage                                                  = messages.StringField(16)
    clinical_T                                                      = messages.StringField(17)
    colorectal_cancer                                               = messages.StringField(18)
    country                                                         = messages.StringField(19)
    country_of_procurement                                          = messages.StringField(20)
    days_to_birth                                                   = messages.IntegerField(21)
    days_to_collection                                              = messages.IntegerField(22)
    days_to_death                                                   = messages.IntegerField(23)
    days_to_initial_pathologic_diagnosis                            = messages.IntegerField(24)
    days_to_last_followup                                           = messages.IntegerField(25)
    days_to_submitted_specimen_dx                                   = messages.IntegerField(26)
    Study                                                           = messages.StringField(27)
    ethnicity                                                       = messages.StringField(28)
    frozen_specimen_anatomic_site                                   = messages.StringField(29)
    gender                                                          = messages.StringField(30)
    height                                                          = messages.IntegerField(31)
    histological_type                                               = messages.StringField(32)
    history_of_colon_polyps                                         = messages.StringField(33)
    history_of_neoadjuvant_treatment                                = messages.StringField(34)
    history_of_prior_malignancy                                     = messages.StringField(35)
    hpv_calls                                                       = messages.StringField(36)
    hpv_status                                                      = messages.StringField(37)
    icd_10                                                          = messages.StringField(38)
    icd_o_3_histology                                               = messages.StringField(39)
    icd_o_3_site                                                    = messages.StringField(40)
    lymph_node_examined_count                                       = messages.IntegerField(41)
    lymphatic_invasion                                              = messages.StringField(42)
    lymphnodes_examined                                             = messages.StringField(43)
    lymphovascular_invasion_present                                 = messages.StringField(44)
    max_percent_lymphocyte_infiltration                             = messages.FloatField(45)
    max_percent_monocyte_infiltration                               = messages.FloatField(46)
    max_percent_necrosis                                            = messages.FloatField(47)
    max_percent_neutrophil_infiltration                             = messages.FloatField(48)
    max_percent_normal_cells                                        = messages.FloatField(49)
    max_percent_stromal_cells                                       = messages.FloatField(50)
    max_percent_tumor_cells                                         = messages.FloatField(51)
    max_percent_tumor_nuclei                                        = messages.FloatField(52)
    menopause_status                                                = messages.StringField(53)
    min_percent_lymphocyte_infiltration                             = messages.FloatField(54)
    min_percent_monocyte_infiltration                               = messages.FloatField(55)
    min_percent_necrosis                                            = messages.FloatField(56)
    min_percent_neutrophil_infiltration                             = messages.FloatField(57)
    min_percent_normal_cells                                        = messages.FloatField(58)
    min_percent_stromal_cells                                       = messages.FloatField(59)
    min_percent_tumor_cells                                         = messages.FloatField(60)
    min_percent_tumor_nuclei                                        = messages.FloatField(61)
    mononucleotide_and_dinucleotide_marker_panel_analysis_status    = messages.StringField(62)
    mononucleotide_marker_panel_analysis_status                     = messages.StringField(63)
    neoplasm_histologic_grade                                       = messages.StringField(64)
    new_tumor_event_after_initial_treatment                         = messages.StringField(65)
    number_of_lymphnodes_examined                                   = messages.IntegerField(66)
    number_of_lymphnodes_positive_by_he                             = messages.IntegerField(67)
    ParticipantBarcode                                              = messages.StringField(68)
    pathologic_M                                                    = messages.StringField(69)
    pathologic_N                                                    = messages.StringField(70)
    pathologic_stage                                                = messages.StringField(71)
    pathologic_T                                                    = messages.StringField(72)
    person_neoplasm_cancer_status                                   = messages.StringField(73)
    pregnancies                                                     = messages.StringField(74)
    preservation_method                                             = messages.StringField(75)
    primary_neoplasm_melanoma_dx                                    = messages.StringField(76)
    primary_therapy_outcome_success                                 = messages.StringField(77)
    prior_dx                                                        = messages.StringField(78)
    Project                                                         = messages.StringField(79)
    psa_value                                                       = messages.FloatField(80)
    race                                                            = messages.StringField(81)
    residual_tumor                                                  = messages.StringField(82)
    SampleBarcode                                                   = messages.StringField(83)
    tobacco_smoking_history                                         = messages.StringField(86)
    total_number_of_pregnancies                                     = messages.IntegerField(87)
    tumor_tissue_site                                               = messages.StringField(88)
    tumor_pathology                                                 = messages.StringField(89)
    tumor_type                                                      = messages.StringField(90)
    weiss_venous_invasion                                           = messages.StringField(91)
    vital_status                                                    = messages.StringField(92)
    weight                                                          = messages.IntegerField(93)
    year_of_initial_pathologic_diagnosis                            = messages.StringField(94)
    SampleTypeCode                                                  = messages.StringField(95)


class CohortsGetListQueryBuilder(object):
    def build_cohort_query(self, query_dict):
        """
        Builds the query that will select cohort id, name, last_date_saved,
        perms, comments, source type, and source notes
        :param query_dict: should contain {'cohorts_cohort_perms.user_id': user_id, 'cohorts_cohort.active': unicode('1')}
        :return: query_str, query_tuple
        """
        query_str = 'SELECT cohorts_cohort.id, ' \
                    'cohorts_cohort.name, ' \
                    'cohorts_cohort.last_date_saved, ' \
                    'cohorts_cohort_perms.perm, ' \
                    'auth_user.email, ' \
                    'cohorts_cohort_comments.content AS comments, ' \
                    'cohorts_source.type AS source_type, ' \
                    'cohorts_source.notes AS source_notes ' \
                    'FROM cohorts_cohort_perms ' \
                    'JOIN cohorts_cohort ' \
                    'ON cohorts_cohort.id=cohorts_cohort_perms.cohort_id ' \
                    'JOIN auth_user ' \
                    'ON auth_user.id=cohorts_cohort_perms.user_id ' \
                    'LEFT JOIN cohorts_cohort_comments ' \
                    'ON cohorts_cohort_comments.user_id=cohorts_cohort_perms.user_id ' \
                    'LEFT JOIN cohorts_source ' \
                    'ON cohorts_source.cohort_id=cohorts_cohort_perms.cohort_id '

        query_tuple = ()
        if query_dict:
            query_str += ' WHERE ' + '=%s and '.join(key for key in query_dict.keys()) + '=%s '
            query_tuple = tuple(value for value in query_dict.values())

        query_str += 'GROUP BY ' \
                     'cohorts_cohort.id,  ' \
                     'cohorts_cohort.name,  ' \
                     'cohorts_cohort.last_date_saved,  ' \
                     'cohorts_cohort_perms.perm,  ' \
                     'auth_user.email,  ' \
                     'comments,  ' \
                     'source_type,  ' \
                     'source_notes '

        return query_str, query_tuple

    def build_filter_query(self, filter_query_dict):
        """
        Builds the query that selects the filter name and value for a particular cohort
        :param filter_query_dict: should be {'cohorts_filters.resulting_cohort_id:': id}
        :return: filter_query_str, filter_query_tuple
        """
        filter_query_str = 'SELECT name, value ' \
                           'FROM cohorts_filters '

        filter_query_str += ' WHERE ' + '=%s AND '.join(key for key in filter_query_dict.keys()) + '=%s '
        filter_query_tuple = tuple(value for value in filter_query_dict.values())

        return filter_query_str, filter_query_tuple

    def build_parent_query(self, parent_query_dict):
        """
        Builds the query that selects parent_ids for a particular cohort
        :param parent_query_dict: should be {'cohort_id': str(row['id'])}
        :return: parent_query_str, parent_query_tuple
        """
        parent_query_str = 'SELECT parent_id ' \
                           'FROM cohorts_source '
        parent_query_str += ' WHERE ' + '=%s AND '.join(key for key in parent_query_dict.keys()) + '=%s '
        parent_query_tuple = tuple(value for value in parent_query_dict.values())

        return parent_query_str, parent_query_tuple

    def build_patients_query(self, patient_query_dict):
        """
        Builds the query that selects the patient count for a particular cohort
        :param patient_query_dict: should be {'cohort_id': str(row['id])}
        :return: patient_query_str, patient_query_tuple
        """
        patients_query_str = 'SELECT patient_id ' \
                             'FROM cohorts_patients '

        patients_query_str += ' WHERE ' + '=%s AND '.join(key for key in patient_query_dict.keys()) + '=%s '
        patient_query_tuple = tuple(value for value in patient_query_dict.values())

        return patients_query_str, patient_query_tuple

    def build_samples_query(self, sample_query_dict):
        """
        Builds the query that selects the sample count for a particular cohort
        :param sample_query_dict: should be {'cohort_id': str(row['id])}
        :return: sample_query_str, sample_query_tuple
        """
        samples_query_str = 'SELECT sample_id ' \
                            'FROM cohorts_samples '

        samples_query_str += ' WHERE ' + '=%s AND '.join(key for key in sample_query_dict.keys()) + '=%s '
        sample_query_tuple = tuple(value for value in sample_query_dict.values())

        return samples_query_str, sample_query_tuple


class CohortsCreatePreviewQueryBuilder(object):
    def build_query_dictionaries(self, request):
        """
        Builds the query dictionaries for create and preview cohort endpoints.
        Returns query_dict, gte_query_dict, lte_query_dict.
        """
        query_dict = {
            k.name: request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name)
            and k.name is not 'name'
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

        return query_dict, gte_query_dict, lte_query_dict

    def build_query(self, query_dict, gte_query_dict, lte_query_dict):
        """
        Builds the queries that selects the patient and sample barcodes
        that meet the criteria specified in the request body.
        Returns patient query string,  sample query string, value tuple.
        """

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
                    patient_query_str += ' OR {key} IN ({vals}) '.format(
                        key=key, vals=', '.join(['%s'] * len(value_list)))
                    sample_query_str += ' OR {key} IN ({vals}) '.format(
                        key=key, vals=', '.join(['%s'] * len(value_list)))
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

        return patient_query_str, sample_query_str, value_tuple


class FilterDetails(messages.Message):
    name = messages.StringField(1)
    value = messages.StringField(2)


class CohortsGetListMessageBuilder(object):
    def make_filter_details_from_cursor(self, filter_cursor_dict):
        """
        Returns list of FilterDetails from a dictionary of results
        from a filter query.
        """
        filter_data = []
        for filter_row in filter_cursor_dict:
            filter_data.append(FilterDetails(
                name=str(filter_row['name']),
                value=str(filter_row['value'])
            ))

        if len(filter_data) == 0:
            filter_data.append(FilterDetails(
                name="None",
                value="None"
            ))

        return filter_data

    def make_parent_id_list_from_cursor(self, parent_cursor_dict, row):
        """
        Returns list of parent_id's from a dictionary of results
        from a parent id query.
        """
        parent_id_data = [str(p_row['parent_id']) for p_row in parent_cursor_dict if row.get('parent_id')]
        if len(parent_id_data) == 0:
            parent_id_data.append("None")

        return parent_id_data


class CohortsSamplesFilesQueryBuilder(object):

    def build_query(self, platform=None, pipeline=None, limit=None, cohort_id=None, sample_barcode=None):

        query_str = 'SELECT DataFileNameKey, SecurityProtocol, Repository ' \
                    'FROM metadata_data '

        if cohort_id is None:
            query_str += 'WHERE SampleBarcode=%s '
        else:
            query_str += 'JOIN cohorts_samples ON metadata_data.SampleBarcode=cohorts_samples.sample_id ' \
                         'WHERE cohorts_samples.cohort_id=%s '

        query_str += 'AND DataFileNameKey != "" AND DataFileNameKey is not null '
        query_str += ' and metadata_data.Platform=%s ' if platform is not None else ''
        query_str += ' and metadata_data.Pipeline=%s ' if pipeline is not None else ''
        query_str += ' GROUP BY DataFileNameKey, SecurityProtocol, Repository '
        query_str += ' LIMIT %s' if limit is not None else ' LIMIT 10000'

        query_tuple = (cohort_id,) if cohort_id is not None else (sample_barcode,)
        query_tuple += (platform,) if platform is not None else ()
        query_tuple += (pipeline,) if pipeline is not None else ()
        query_tuple += (limit,) if limit is not None else ()

        return query_str, query_tuple


class CohortsSamplesFilesMessageBuilder(object):

    def get_files_and_bad_repos(self, cursor_rows):
        datafilenamekeys = []
        bad_repo_count = 0
        bad_repo_set = set()
        for row in cursor_rows:
            if not row.get('DataFileNameKey'):
                continue

            if 'controlled' not in str(row['SecurityProtocol']).lower():
                # this may only be necessary for the vagrant db
                path = row.get('DataFileNameKey') if row.get('DataFileNameKey') is None \
                    else row.get('DataFileNameKey').replace('gs://' + settings.OPEN_DATA_BUCKET, '')
                datafilenamekeys.append(
                    "gs://{}{}".format(settings.OPEN_DATA_BUCKET, path))
            else:  # not filtering on dbGaP_authorized
                if row['Repository'].lower() == 'dcc':
                    bucket_name = settings.DCC_CONTROLLED_DATA_BUCKET
                elif row['Repository'].lower() == 'cghub':
                    bucket_name = settings.CGHUB_CONTROLLED_DATA_BUCKET
                else:  # shouldn't ever happen
                    bad_repo_count += 1
                    bad_repo_set.add(row['Repository'])
                    continue
                # this may only be necessary for the vagrant db
                path = row.get('DataFileNameKey') if row.get('DataFileNameKey') is None \
                    else row.get('DataFileNameKey').replace('gs://' + bucket_name, '')
                datafilenamekeys.append("gs://{}{}".format(bucket_name, path))
        return datafilenamekeys, bad_repo_count, bad_repo_set