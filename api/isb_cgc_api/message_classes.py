from protorpc import messages


class MetadataRangesItem(messages.Message):
    
    age_at_initial_pathologic_diagnosis                               = messages.IntegerField(1, repeated=True, variant=messages.Variant.INT32)
    age_at_initial_pathologic_diagnosis_lte                           = messages.IntegerField(2, repeated=True, variant=messages.Variant.INT32)
    age_at_initial_pathologic_diagnosis_gte                           = messages.IntegerField(3, repeated=True, variant=messages.Variant.INT32)
    
    anatomic_neoplasm_subdivision                                     = messages.StringField(4, repeated=True)
    
    avg_percent_lymphocyte_infiltration                               = messages.FloatField(5, repeated=True)
    avg_percent_lymphocyte_infiltration_lte                           = messages.FloatField(6, repeated=True)
    avg_percent_lymphocyte_infiltration_gte                           = messages.FloatField(7, repeated=True)
    
    
    avg_percent_monocyte_infiltration                                 = messages.FloatField(8, repeated=True)
    avg_percent_monocyte_infiltration_lte                             = messages.FloatField(9, repeated=True)
    avg_percent_monocyte_infiltration_gte                             = messages.FloatField(10, repeated=True)
    
    
    avg_percent_necrosis                                              = messages.FloatField(11, repeated=True)
    avg_percent_necrosis_lte                                          = messages.FloatField(12, repeated=True)
    avg_percent_necrosis_gte                                          = messages.FloatField(13, repeated=True)
    
    
    avg_percent_neutrophil_infiltration                               = messages.FloatField(14, repeated=True)
    avg_percent_neutrophil_infiltration_lte                           = messages.FloatField(15, repeated=True)
    avg_percent_neutrophil_infiltration_gte                           = messages.FloatField(16, repeated=True)
    
    
    avg_percent_normal_cells                                          = messages.FloatField(17, repeated=True)
    avg_percent_normal_cells_lte                                      = messages.FloatField(18, repeated=True)
    avg_percent_normal_cells_gte                                      = messages.FloatField(19, repeated=True)
    
    
    avg_percent_stromal_cells                                         = messages.FloatField(20, repeated=True)
    avg_percent_stromal_cells_lte                                     = messages.FloatField(21, repeated=True)
    avg_percent_stromal_cells_gte                                     = messages.FloatField(22, repeated=True)
    
    
    avg_percent_tumor_cells                                           = messages.FloatField(23, repeated=True)
    avg_percent_tumor_cells_lte                                       = messages.FloatField(24, repeated=True)
    avg_percent_tumor_cells_gte                                       = messages.FloatField(25, repeated=True)
    
    
    avg_percent_tumor_nuclei                                          = messages.FloatField(26, repeated=True)
    avg_percent_tumor_nuclei_lte                                      = messages.FloatField(27, repeated=True)
    avg_percent_tumor_nuclei_gte                                      = messages.FloatField(28, repeated=True)
    
    
    batch_number                                                      = messages.IntegerField(29, repeated=True, variant=messages.Variant.INT32)
    batch_number_lte                                                  = messages.IntegerField(30, repeated=True, variant=messages.Variant.INT32)
    batch_number_gte                                                  = messages.IntegerField(31, repeated=True, variant=messages.Variant.INT32)
    
    bcr                                                               = messages.StringField(32, repeated=True)
    
    BMI                                                               = messages.FloatField(33, repeated=True)
    BMI_lte                                                           = messages.FloatField(34, repeated=True)
    BMI_gte                                                           = messages.FloatField(35, repeated=True)
    
    clinical_M                                                        = messages.StringField(36, repeated=True)
    clinical_N                                                        = messages.StringField(37, repeated=True)
    clinical_stage                                                    = messages.StringField(38, repeated=True)
    clinical_T                                                        = messages.StringField(39, repeated=True)
    colorectal_cancer                                                 = messages.StringField(40, repeated=True)
    country                                                           = messages.StringField(41, repeated=True)
    
    days_to_birth                                                     = messages.IntegerField(42, repeated=True, variant=messages.Variant.INT32)
    days_to_birth_lte                                                 = messages.IntegerField(43, repeated=True, variant=messages.Variant.INT32)
    days_to_birth_gte                                                 = messages.IntegerField(44, repeated=True, variant=messages.Variant.INT32)
    
    
    days_to_collection                                                = messages.IntegerField(45, repeated=True, variant=messages.Variant.INT32)
    days_to_collection_lte                                            = messages.IntegerField(46, repeated=True, variant=messages.Variant.INT32)
    days_to_collection_gte                                            = messages.IntegerField(47, repeated=True, variant=messages.Variant.INT32)
    
    
    days_to_death                                                     = messages.IntegerField(48, repeated=True, variant=messages.Variant.INT32)
    days_to_death_lte                                                 = messages.IntegerField(49, repeated=True, variant=messages.Variant.INT32)
    days_to_death_gte                                                 = messages.IntegerField(50, repeated=True, variant=messages.Variant.INT32)
    
    
    days_to_initial_pathologic_diagnosis                              = messages.IntegerField(51, repeated=True, variant=messages.Variant.INT32)
    days_to_initial_pathologic_diagnosis_lte                          = messages.IntegerField(52, repeated=True, variant=messages.Variant.INT32)
    days_to_initial_pathologic_diagnosis_gte                          = messages.IntegerField(53, repeated=True, variant=messages.Variant.INT32)
    
    
    days_to_last_followup                                             = messages.IntegerField(54, repeated=True, variant=messages.Variant.INT32)
    days_to_last_followup_lte                                         = messages.IntegerField(55, repeated=True, variant=messages.Variant.INT32)
    days_to_last_followup_gte                                         = messages.IntegerField(56, repeated=True, variant=messages.Variant.INT32)
    
    
    days_to_last_known_alive                                          = messages.IntegerField(57, repeated=True, variant=messages.Variant.INT32)
    days_to_last_known_alive_lte                                      = messages.IntegerField(58, repeated=True, variant=messages.Variant.INT32)
    days_to_last_known_alive_gte                                      = messages.IntegerField(59, repeated=True, variant=messages.Variant.INT32)
    
    
    days_to_submitted_specimen_dx                                     = messages.IntegerField(60, repeated=True, variant=messages.Variant.INT32)
    days_to_submitted_specimen_dx_lte                                 = messages.IntegerField(61, repeated=True, variant=messages.Variant.INT32)
    days_to_submitted_specimen_dx_gte                                 = messages.IntegerField(62, repeated=True, variant=messages.Variant.INT32)
    
    ethnicity                                                         = messages.StringField(63, repeated=True)
    frozen_specimen_anatomic_site                                     = messages.StringField(64, repeated=True)
    gender                                                            = messages.StringField(65, repeated=True)
    
    gleason_score_combined                                            = messages.IntegerField(66, repeated=True, variant=messages.Variant.INT32)
    gleason_score_combined_lte                                        = messages.IntegerField(67, repeated=True, variant=messages.Variant.INT32)
    gleason_score_combined_gte                                        = messages.IntegerField(68, repeated=True, variant=messages.Variant.INT32)
    
    has_27k                                                           = messages.BooleanField(69, repeated=True)
    has_450k                                                          = messages.BooleanField(70, repeated=True)
    has_BCGSC_GA_RNASeq                                               = messages.BooleanField(71, repeated=True)
    has_BCGSC_HiSeq_RNASeq                                            = messages.BooleanField(72, repeated=True)
    has_GA_miRNASeq                                                   = messages.BooleanField(73, repeated=True)
    has_HiSeq_miRnaSeq                                                = messages.BooleanField(74, repeated=True)
    has_Illumina_DNASeq                                               = messages.BooleanField(75, repeated=True)
    has_RPPA                                                          = messages.BooleanField(76, repeated=True)
    has_SNP6                                                          = messages.BooleanField(77, repeated=True)
    has_UNC_GA_RNASeq                                                 = messages.BooleanField(78, repeated=True)
    has_UNC_HiSeq_RNASeq                                              = messages.BooleanField(79, repeated=True)
    
    height                                                            = messages.IntegerField(80, repeated=True, variant=messages.Variant.INT32)
    height_lte                                                        = messages.IntegerField(81, repeated=True, variant=messages.Variant.INT32)
    height_gte                                                        = messages.IntegerField(82, repeated=True, variant=messages.Variant.INT32)
    
    histological_type                                                 = messages.StringField(83, repeated=True)
    history_of_colon_polyps                                           = messages.StringField(84, repeated=True)
    history_of_neoadjuvant_treatment                                  = messages.StringField(85, repeated=True)
    history_of_prior_malignancy                                       = messages.StringField(86, repeated=True)
    hpv_calls                                                         = messages.StringField(87, repeated=True)
    hpv_status                                                        = messages.StringField(88, repeated=True)
    icd_10                                                            = messages.StringField(89, repeated=True)
    icd_o_3_histology                                                 = messages.StringField(90, repeated=True)
    icd_o_3_site                                                      = messages.StringField(91, repeated=True)
    lymphatic_invasion                                                = messages.StringField(92, repeated=True)
    lymphnodes_examined                                               = messages.StringField(93, repeated=True)
    lymphovascular_invasion_present                                   = messages.StringField(94, repeated=True)
    
    max_percent_lymphocyte_infiltration                               = messages.FloatField(95, repeated=True)
    max_percent_lymphocyte_infiltration_lte                           = messages.FloatField(96, repeated=True)
    max_percent_lymphocyte_infiltration_gte                           = messages.FloatField(97, repeated=True)
    
    
    max_percent_monocyte_infiltration                                 = messages.FloatField(98, repeated=True)
    max_percent_monocyte_infiltration_lte                             = messages.FloatField(99, repeated=True)
    max_percent_monocyte_infiltration_gte                             = messages.FloatField(100, repeated=True)
    
    
    max_percent_necrosis                                              = messages.FloatField(101, repeated=True)
    max_percent_necrosis_lte                                          = messages.FloatField(102, repeated=True)
    max_percent_necrosis_gte                                          = messages.FloatField(103, repeated=True)
    
    
    max_percent_neutrophil_infiltration                               = messages.FloatField(104, repeated=True)
    max_percent_neutrophil_infiltration_lte                           = messages.FloatField(105, repeated=True)
    max_percent_neutrophil_infiltration_gte                           = messages.FloatField(106, repeated=True)
    
    
    max_percent_normal_cells                                          = messages.FloatField(107, repeated=True)
    max_percent_normal_cells_lte                                      = messages.FloatField(108, repeated=True)
    max_percent_normal_cells_gte                                      = messages.FloatField(109, repeated=True)
    
    
    max_percent_stromal_cells                                         = messages.FloatField(110, repeated=True)
    max_percent_stromal_cells_lte                                     = messages.FloatField(111, repeated=True)
    max_percent_stromal_cells_gte                                     = messages.FloatField(112, repeated=True)
    
    
    max_percent_tumor_cells                                           = messages.FloatField(113, repeated=True)
    max_percent_tumor_cells_lte                                       = messages.FloatField(114, repeated=True)
    max_percent_tumor_cells_gte                                       = messages.FloatField(115, repeated=True)
    
    
    max_percent_tumor_nuclei                                          = messages.FloatField(116, repeated=True)
    max_percent_tumor_nuclei_lte                                      = messages.FloatField(117, repeated=True)
    max_percent_tumor_nuclei_gte                                      = messages.FloatField(118, repeated=True)
    
    menopause_status                                                  = messages.StringField(119, repeated=True)
    
    min_percent_lymphocyte_infiltration                               = messages.FloatField(120, repeated=True)
    min_percent_lymphocyte_infiltration_lte                           = messages.FloatField(121, repeated=True)
    min_percent_lymphocyte_infiltration_gte                           = messages.FloatField(122, repeated=True)
    
    
    min_percent_monocyte_infiltration                                 = messages.FloatField(123, repeated=True)
    min_percent_monocyte_infiltration_lte                             = messages.FloatField(124, repeated=True)
    min_percent_monocyte_infiltration_gte                             = messages.FloatField(125, repeated=True)
    
    
    min_percent_necrosis                                              = messages.FloatField(126, repeated=True)
    min_percent_necrosis_lte                                          = messages.FloatField(127, repeated=True)
    min_percent_necrosis_gte                                          = messages.FloatField(128, repeated=True)
    
    
    min_percent_neutrophil_infiltration                               = messages.FloatField(129, repeated=True)
    min_percent_neutrophil_infiltration_lte                           = messages.FloatField(130, repeated=True)
    min_percent_neutrophil_infiltration_gte                           = messages.FloatField(131, repeated=True)
    
    
    min_percent_normal_cells                                          = messages.FloatField(132, repeated=True)
    min_percent_normal_cells_lte                                      = messages.FloatField(133, repeated=True)
    min_percent_normal_cells_gte                                      = messages.FloatField(134, repeated=True)
    
    
    min_percent_stromal_cells                                         = messages.FloatField(135, repeated=True)
    min_percent_stromal_cells_lte                                     = messages.FloatField(136, repeated=True)
    min_percent_stromal_cells_gte                                     = messages.FloatField(137, repeated=True)
    
    
    min_percent_tumor_cells                                           = messages.FloatField(138, repeated=True)
    min_percent_tumor_cells_lte                                       = messages.FloatField(139, repeated=True)
    min_percent_tumor_cells_gte                                       = messages.FloatField(140, repeated=True)
    
    
    min_percent_tumor_nuclei                                          = messages.FloatField(141, repeated=True)
    min_percent_tumor_nuclei_lte                                      = messages.FloatField(142, repeated=True)
    min_percent_tumor_nuclei_gte                                      = messages.FloatField(143, repeated=True)
    
    mononucleotide_and_dinucleotide_marker_panel_analysis_status      = messages.StringField(144, repeated=True)
    mononucleotide_marker_panel_analysis_status                       = messages.StringField(145, repeated=True)
    neoplasm_histologic_grade                                         = messages.StringField(146, repeated=True)
    new_tumor_event_after_initial_treatment                           = messages.StringField(147, repeated=True)
    
    number_of_lymphnodes_examined                                     = messages.IntegerField(148, repeated=True, variant=messages.Variant.INT32)
    number_of_lymphnodes_examined_lte                                 = messages.IntegerField(149, repeated=True, variant=messages.Variant.INT32)
    number_of_lymphnodes_examined_gte                                 = messages.IntegerField(150, repeated=True, variant=messages.Variant.INT32)
    
    
    number_of_lymphnodes_positive_by_he                               = messages.IntegerField(151, repeated=True, variant=messages.Variant.INT32)
    number_of_lymphnodes_positive_by_he_lte                           = messages.IntegerField(152, repeated=True, variant=messages.Variant.INT32)
    number_of_lymphnodes_positive_by_he_gte                           = messages.IntegerField(153, repeated=True, variant=messages.Variant.INT32)
    
    
    number_pack_years_smoked                                          = messages.IntegerField(154, repeated=True, variant=messages.Variant.INT32)
    number_pack_years_smoked_lte                                      = messages.IntegerField(155, repeated=True, variant=messages.Variant.INT32)
    number_pack_years_smoked_gte                                      = messages.IntegerField(156, repeated=True, variant=messages.Variant.INT32)
    
    ParticipantBarcode                                                = messages.StringField(157, repeated=True)
    pathologic_M                                                      = messages.StringField(158, repeated=True)
    pathologic_N                                                      = messages.StringField(159, repeated=True)
    pathologic_stage                                                  = messages.StringField(160, repeated=True)
    pathologic_T                                                      = messages.StringField(161, repeated=True)
    person_neoplasm_cancer_status                                     = messages.StringField(162, repeated=True)
    pregnancies                                                       = messages.StringField(163, repeated=True)
    primary_neoplasm_melanoma_dx                                      = messages.StringField(164, repeated=True)
    primary_therapy_outcome_success                                   = messages.StringField(165, repeated=True)
    prior_dx                                                          = messages.StringField(166, repeated=True)
    Project                                                           = messages.StringField(167, repeated=True)
    
    psa_value                                                         = messages.FloatField(168, repeated=True)
    psa_value_lte                                                     = messages.FloatField(169, repeated=True)
    psa_value_gte                                                     = messages.FloatField(170, repeated=True)
    
    race                                                              = messages.StringField(171, repeated=True)
    residual_tumor                                                    = messages.StringField(172, repeated=True)
    SampleBarcode                                                     = messages.StringField(173, repeated=True)
    SampleTypeCode                                                    = messages.StringField(174, repeated=True)
    Study                                                             = messages.StringField(175, repeated=True)
    tobacco_smoking_history                                           = messages.StringField(176, repeated=True)
    TSSCode                                                           = messages.StringField(177, repeated=True)
    tumor_tissue_site                                                 = messages.StringField(178, repeated=True)
    tumor_type                                                        = messages.StringField(179, repeated=True)
    vital_status                                                      = messages.StringField(180, repeated=True)
    
    weight                                                            = messages.IntegerField(181, repeated=True, variant=messages.Variant.INT32)
    weight_lte                                                        = messages.IntegerField(182, repeated=True, variant=messages.Variant.INT32)
    weight_gte                                                        = messages.IntegerField(183, repeated=True, variant=messages.Variant.INT32)
    
    weiss_venous_invasion                                             = messages.StringField(184, repeated=True)
    
    year_of_initial_pathologic_diagnosis                              = messages.IntegerField(185, repeated=True, variant=messages.Variant.INT32)
    year_of_initial_pathologic_diagnosis_lte                          = messages.IntegerField(186, repeated=True, variant=messages.Variant.INT32)
    year_of_initial_pathologic_diagnosis_gte                          = messages.IntegerField(187, repeated=True, variant=messages.Variant.INT32)

    
class MetadataItem(messages.Message):
    age_at_initial_pathologic_diagnosis                               = messages.IntegerField(1, variant=messages.Variant.INT32)
    anatomic_neoplasm_subdivision                                     = messages.StringField(2)
    avg_percent_lymphocyte_infiltration                               = messages.FloatField(3)
    avg_percent_monocyte_infiltration                                 = messages.FloatField(4)
    avg_percent_necrosis                                              = messages.FloatField(5)
    avg_percent_neutrophil_infiltration                               = messages.FloatField(6)
    avg_percent_normal_cells                                          = messages.FloatField(7)
    avg_percent_stromal_cells                                         = messages.FloatField(8)
    avg_percent_tumor_cells                                           = messages.FloatField(9)
    avg_percent_tumor_nuclei                                          = messages.FloatField(10)
    batch_number                                                      = messages.IntegerField(11, variant=messages.Variant.INT32)
    bcr                                                               = messages.StringField(12)
    BMI                                                               = messages.FloatField(13)
    clinical_M                                                        = messages.StringField(14)
    clinical_N                                                        = messages.StringField(15)
    clinical_stage                                                    = messages.StringField(16)
    clinical_T                                                        = messages.StringField(17)
    colorectal_cancer                                                 = messages.StringField(18)
    country                                                           = messages.StringField(19)
    days_to_birth                                                     = messages.IntegerField(20, variant=messages.Variant.INT32)
    days_to_collection                                                = messages.IntegerField(21, variant=messages.Variant.INT32)
    days_to_death                                                     = messages.IntegerField(22, variant=messages.Variant.INT32)
    days_to_initial_pathologic_diagnosis                              = messages.IntegerField(23, variant=messages.Variant.INT32)
    days_to_last_followup                                             = messages.IntegerField(24, variant=messages.Variant.INT32)
    days_to_last_known_alive                                          = messages.IntegerField(25, variant=messages.Variant.INT32)
    days_to_submitted_specimen_dx                                     = messages.IntegerField(26, variant=messages.Variant.INT32)
    ethnicity                                                         = messages.StringField(27)
    frozen_specimen_anatomic_site                                     = messages.StringField(28)
    gender                                                            = messages.StringField(29)
    gleason_score_combined                                            = messages.IntegerField(30, variant=messages.Variant.INT32)
    has_27k                                                           = messages.BooleanField(31)
    has_450k                                                          = messages.BooleanField(32)
    has_BCGSC_GA_RNASeq                                               = messages.BooleanField(33)
    has_BCGSC_HiSeq_RNASeq                                            = messages.BooleanField(34)
    has_GA_miRNASeq                                                   = messages.BooleanField(35)
    has_HiSeq_miRnaSeq                                                = messages.BooleanField(36)
    has_Illumina_DNASeq                                               = messages.BooleanField(37)
    has_RPPA                                                          = messages.BooleanField(38)
    has_SNP6                                                          = messages.BooleanField(39)
    has_UNC_GA_RNASeq                                                 = messages.BooleanField(40)
    has_UNC_HiSeq_RNASeq                                              = messages.BooleanField(41)
    height                                                            = messages.IntegerField(42, variant=messages.Variant.INT32)
    histological_type                                                 = messages.StringField(43)
    history_of_colon_polyps                                           = messages.StringField(44)
    history_of_neoadjuvant_treatment                                  = messages.StringField(45)
    history_of_prior_malignancy                                       = messages.StringField(46)
    hpv_calls                                                         = messages.StringField(47)
    hpv_status                                                        = messages.StringField(48)
    icd_10                                                            = messages.StringField(49)
    icd_o_3_histology                                                 = messages.StringField(50)
    icd_o_3_site                                                      = messages.StringField(51)
    lymphatic_invasion                                                = messages.StringField(52)
    lymphnodes_examined                                               = messages.StringField(53)
    lymphovascular_invasion_present                                   = messages.StringField(54)
    max_percent_lymphocyte_infiltration                               = messages.FloatField(55)
    max_percent_monocyte_infiltration                                 = messages.FloatField(56)
    max_percent_necrosis                                              = messages.FloatField(57)
    max_percent_neutrophil_infiltration                               = messages.FloatField(58)
    max_percent_normal_cells                                          = messages.FloatField(59)
    max_percent_stromal_cells                                         = messages.FloatField(60)
    max_percent_tumor_cells                                           = messages.FloatField(61)
    max_percent_tumor_nuclei                                          = messages.FloatField(62)
    menopause_status                                                  = messages.StringField(63)
    min_percent_lymphocyte_infiltration                               = messages.FloatField(64)
    min_percent_monocyte_infiltration                                 = messages.FloatField(65)
    min_percent_necrosis                                              = messages.FloatField(66)
    min_percent_neutrophil_infiltration                               = messages.FloatField(67)
    min_percent_normal_cells                                          = messages.FloatField(68)
    min_percent_stromal_cells                                         = messages.FloatField(69)
    min_percent_tumor_cells                                           = messages.FloatField(70)
    min_percent_tumor_nuclei                                          = messages.FloatField(71)
    mononucleotide_and_dinucleotide_marker_panel_analysis_status      = messages.StringField(72)
    mononucleotide_marker_panel_analysis_status                       = messages.StringField(73)
    neoplasm_histologic_grade                                         = messages.StringField(74)
    new_tumor_event_after_initial_treatment                           = messages.StringField(75)
    number_of_lymphnodes_examined                                     = messages.IntegerField(76, variant=messages.Variant.INT32)
    number_of_lymphnodes_positive_by_he                               = messages.IntegerField(77, variant=messages.Variant.INT32)
    number_pack_years_smoked                                          = messages.IntegerField(78, variant=messages.Variant.INT32)
    ParticipantBarcode                                                = messages.StringField(79)
    pathologic_M                                                      = messages.StringField(80)
    pathologic_N                                                      = messages.StringField(81)
    pathologic_stage                                                  = messages.StringField(82)
    pathologic_T                                                      = messages.StringField(83)
    person_neoplasm_cancer_status                                     = messages.StringField(84)
    pregnancies                                                       = messages.StringField(85)
    primary_neoplasm_melanoma_dx                                      = messages.StringField(86)
    primary_therapy_outcome_success                                   = messages.StringField(87)
    prior_dx                                                          = messages.StringField(88)
    Project                                                           = messages.StringField(89)
    psa_value                                                         = messages.FloatField(90)
    race                                                              = messages.StringField(91)
    residual_tumor                                                    = messages.StringField(92)
    SampleBarcode                                                     = messages.StringField(93)
    SampleTypeCode                                                    = messages.StringField(94)
    Study                                                             = messages.StringField(95)
    tobacco_smoking_history                                           = messages.StringField(96)
    TSSCode                                                           = messages.StringField(97)
    tumor_tissue_site                                                 = messages.StringField(98)
    tumor_type                                                        = messages.StringField(99)
    vital_status                                                      = messages.StringField(100)
    weight                                                            = messages.IntegerField(101, variant=messages.Variant.INT32)
    weiss_venous_invasion                                             = messages.StringField(102)
    year_of_initial_pathologic_diagnosis                              = messages.IntegerField(103, variant=messages.Variant.INT32)