import endpoints
from django.conf import settings
from protorpc import messages

INSTALLED_APP_CLIENT_ID = settings.INSTALLED_APP_CLIENT_ID
CONTROLLED_ACL_GOOGLE_GROUP = settings.ACL_GOOGLE_GROUP
# WEB_CLIENT_ID = settings.GOOGLE_CLIENT_ID

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
                                  allowed_client_ids=[INSTALLED_APP_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID, settings.WEB_CLIENT_ID])

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