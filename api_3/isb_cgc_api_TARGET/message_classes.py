from protorpc import messages

class CommonMetadataRangesItem(messages.Message):
    disease_code                                                      = messages.StringField(1, repeated=True)
    endpoint_type                                                     = messages.StringField(2, repeated=True)
    program_name                                                      = messages.StringField(3, repeated=True)
    project_short_name                                                = messages.StringField(4, repeated=True)
    
class CommonMetadataItem(messages.Message):
    disease_code                                                      = messages.StringField(1)
    endpoint_type                                                     = messages.StringField(2)
    program_name                                                      = messages.StringField(3)
    project_short_name                                                = messages.StringField(4)
    
class ClinicalMetadataRangesItem(messages.Message):
    age_at_diagnosis                                                  = messages.IntegerField(1, repeated=True, variant=messages.Variant.INT32)
    age_at_diagnosis_lte                                              = messages.IntegerField(2, variant=messages.Variant.INT32)
    age_at_diagnosis_gte                                              = messages.IntegerField(3, variant=messages.Variant.INT32)
    
    case_barcode                                                      = messages.StringField(4, repeated=True)
    case_gdc_id                                                       = messages.StringField(5, repeated=True)
    days_to_birth                                                     = messages.IntegerField(6, repeated=True, variant=messages.Variant.INT32)
    days_to_birth_lte                                                 = messages.IntegerField(7, variant=messages.Variant.INT32)
    days_to_birth_gte                                                 = messages.IntegerField(8, variant=messages.Variant.INT32)
    
    days_to_death                                                     = messages.IntegerField(9, repeated=True, variant=messages.Variant.INT32)
    days_to_death_lte                                                 = messages.IntegerField(10, variant=messages.Variant.INT32)
    days_to_death_gte                                                 = messages.IntegerField(11, variant=messages.Variant.INT32)
    
    days_to_last_followup                                             = messages.IntegerField(12, repeated=True, variant=messages.Variant.INT32)
    days_to_last_followup_lte                                         = messages.IntegerField(13, variant=messages.Variant.INT32)
    days_to_last_followup_gte                                         = messages.IntegerField(14, variant=messages.Variant.INT32)
    
    days_to_last_known_alive                                          = messages.IntegerField(15, repeated=True, variant=messages.Variant.INT32)
    days_to_last_known_alive_lte                                      = messages.IntegerField(16, variant=messages.Variant.INT32)
    days_to_last_known_alive_gte                                      = messages.IntegerField(17, variant=messages.Variant.INT32)
    
    ethnicity                                                         = messages.StringField(18, repeated=True)
    event_free_survival                                               = messages.IntegerField(19, repeated=True, variant=messages.Variant.INT32)
    event_free_survival_lte                                           = messages.IntegerField(20, variant=messages.Variant.INT32)
    event_free_survival_gte                                           = messages.IntegerField(21, variant=messages.Variant.INT32)
    
    first_event                                                       = messages.StringField(22, repeated=True)
    gender                                                            = messages.StringField(23, repeated=True)
    protocol                                                          = messages.StringField(24, repeated=True)
    race                                                              = messages.StringField(25, repeated=True)
    summary_file_count                                                = messages.IntegerField(26, repeated=True, variant=messages.Variant.INT32)
    summary_file_count_lte                                            = messages.IntegerField(27, variant=messages.Variant.INT32)
    summary_file_count_gte                                            = messages.IntegerField(28, variant=messages.Variant.INT32)
    
    vital_status                                                      = messages.StringField(29, repeated=True)
    wbc_at_diagnosis                                                  = messages.FloatField(30, repeated=True)
    wbc_at_diagnosis_lte                                              = messages.FloatField(31)
    wbc_at_diagnosis_gte                                              = messages.FloatField(32)
    
    year_of_diagnosis                                                 = messages.IntegerField(33, repeated=True, variant=messages.Variant.INT32)
    year_of_diagnosis_lte                                             = messages.IntegerField(34, variant=messages.Variant.INT32)
    year_of_diagnosis_gte                                             = messages.IntegerField(35, variant=messages.Variant.INT32)
    
    year_of_last_follow_up                                            = messages.IntegerField(36, repeated=True, variant=messages.Variant.INT32)
    year_of_last_follow_up_lte                                        = messages.IntegerField(37, variant=messages.Variant.INT32)
    year_of_last_follow_up_gte                                        = messages.IntegerField(38, variant=messages.Variant.INT32)
    
    
class ClinicalMetadataItem(messages.Message):
    age_at_diagnosis                                                  = messages.IntegerField(1, variant=messages.Variant.INT32)
    case_barcode                                                      = messages.StringField(2)
    case_gdc_id                                                       = messages.StringField(3)
    days_to_birth                                                     = messages.IntegerField(4, variant=messages.Variant.INT32)
    days_to_death                                                     = messages.IntegerField(5, variant=messages.Variant.INT32)
    days_to_last_followup                                             = messages.IntegerField(6, variant=messages.Variant.INT32)
    days_to_last_known_alive                                          = messages.IntegerField(7, variant=messages.Variant.INT32)
    ethnicity                                                         = messages.StringField(8)
    event_free_survival                                               = messages.IntegerField(9, variant=messages.Variant.INT32)
    first_event                                                       = messages.StringField(10)
    gender                                                            = messages.StringField(11)
    protocol                                                          = messages.StringField(12)
    race                                                              = messages.StringField(13)
    summary_file_count                                                = messages.IntegerField(14, variant=messages.Variant.INT32)
    vital_status                                                      = messages.StringField(15)
    wbc_at_diagnosis                                                  = messages.FloatField(16)
    year_of_diagnosis                                                 = messages.IntegerField(17, variant=messages.Variant.INT32)
    year_of_last_follow_up                                            = messages.IntegerField(18, variant=messages.Variant.INT32)
    
class BiospecimenMetadataRangesItem(messages.Message):
    case_barcode                                                      = messages.StringField(1, repeated=True)
    case_gdc_id                                                       = messages.StringField(2, repeated=True)
    sample_barcode                                                    = messages.StringField(3, repeated=True)
    sample_gdc_id                                                     = messages.StringField(4, repeated=True)
    sample_type                                                       = messages.StringField(5, repeated=True)
    tumor_code                                                        = messages.StringField(6, repeated=True)
    
class BiospecimenMetadataItem(messages.Message):
    case_barcode                                                      = messages.StringField(1)
    case_gdc_id                                                       = messages.StringField(2)
    sample_barcode                                                    = messages.StringField(3)
    sample_gdc_id                                                     = messages.StringField(4)
    sample_type                                                       = messages.StringField(5)
    tumor_code                                                        = messages.StringField(6)
    
class Data_HG19MetadataRangesItem(messages.Message):
    access                                                            = messages.StringField(1, repeated=True)
    case_barcode                                                      = messages.StringField(5, repeated=True)
    case_gdc_id                                                       = messages.StringField(6, repeated=True)
    data_category                                                     = messages.StringField(10, repeated=True)
    data_format                                                       = messages.StringField(11, repeated=True)
    data_type                                                         = messages.StringField(12, repeated=True)
    experimental_strategy                                             = messages.StringField(13, repeated=True)
    file_name_key                                                         = messages.StringField(14, repeated=True)
    index_file_name_key                                                   = messages.StringField(17, repeated=True)
    platform                                                          = messages.StringField(18, repeated=True)
    sample_barcode                                                    = messages.StringField(19, repeated=True)
    sample_gdc_id                                                     = messages.StringField(20, repeated=True)
    sample_type                                                       = messages.StringField(21, repeated=True)
    
class Data_HG19MetadataItem(messages.Message):
    access                                                            = messages.StringField(1)
    case_barcode                                                      = messages.StringField(5)
    case_gdc_id                                                       = messages.StringField(6)
    data_category                                                     = messages.StringField(10)
    data_format                                                       = messages.StringField(11)
    data_type                                                         = messages.StringField(12)
    experimental_strategy                                             = messages.StringField(13)
    file_name_key                                                         = messages.StringField(14)
    index_file_name_key                                                   = messages.StringField(17)
    platform                                                          = messages.StringField(18)
    sample_barcode                                                    = messages.StringField(19)
    sample_gdc_id                                                     = messages.StringField(20)
    sample_type                                                       = messages.StringField(21)
    
class Data_HG38MetadataRangesItem(messages.Message):
    access                                                            = messages.StringField(1, repeated=True)
    case_barcode                                                      = messages.StringField(5, repeated=True)
    case_gdc_id                                                       = messages.StringField(6, repeated=True)
    data_category                                                     = messages.StringField(10, repeated=True)
    data_format                                                       = messages.StringField(11, repeated=True)
    data_type                                                         = messages.StringField(12, repeated=True)
    experimental_strategy                                             = messages.StringField(13, repeated=True)
    file_name_key                                                         = messages.StringField(14, repeated=True)
    index_file_name_key                                                   = messages.StringField(17, repeated=True)
    platform                                                          = messages.StringField(18, repeated=True)
    sample_barcode                                                    = messages.StringField(19, repeated=True)
    sample_gdc_id                                                     = messages.StringField(20, repeated=True)
    sample_type                                                       = messages.StringField(21, repeated=True)
    
class Data_HG38MetadataItem(messages.Message):
    access                                                            = messages.StringField(1)
    case_barcode                                                      = messages.StringField(5)
    case_gdc_id                                                       = messages.StringField(6)
    data_category                                                     = messages.StringField(10)
    data_format                                                       = messages.StringField(11)
    data_type                                                         = messages.StringField(12)
    experimental_strategy                                             = messages.StringField(13)
    file_name_key                                                         = messages.StringField(14)
    index_file_name_key                                                   = messages.StringField(17)
    platform                                                          = messages.StringField(18)
    sample_barcode                                                    = messages.StringField(19)
    sample_gdc_id                                                     = messages.StringField(20)
    sample_type                                                       = messages.StringField(21)
    
class MetadataRangesItem(messages.Message):
    Common = messages.MessageField(CommonMetadataRangesItem, 1)
    Clinical = messages.MessageField(ClinicalMetadataRangesItem, 2)
    Biospecimen = messages.MessageField(BiospecimenMetadataRangesItem, 3)
    Data_HG19 = messages.MessageField(Data_HG19MetadataRangesItem, 4)
    Data_HG38 = messages.MessageField(Data_HG38MetadataRangesItem, 5)

class MetadataItem(messages.Message):
    Common = messages.MessageField(CommonMetadataItem, 1)
    Clinical = messages.MessageField(ClinicalMetadataItem, 2)
    Biospecimen = messages.MessageField(BiospecimenMetadataItem, 3)
    Data_HG19 = messages.MessageField(Data_HG19MetadataItem, 4)
    Data_HG38 = messages.MessageField(Data_HG38MetadataItem, 5)

