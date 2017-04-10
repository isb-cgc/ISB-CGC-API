from protorpc import messages

class MetadataRangesItem(messages.Message):
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
    
    endpoint_type                                                     = messages.StringField(12, repeated=True)
    ethnicity                                                         = messages.StringField(13, repeated=True)
    event_free_survival                                               = messages.IntegerField(14, repeated=True, variant=messages.Variant.INT32)
    event_free_survival_lte                                           = messages.IntegerField(15, variant=messages.Variant.INT32)
    event_free_survival_gte                                           = messages.IntegerField(16, variant=messages.Variant.INT32)
    
    first_event                                                       = messages.StringField(17, repeated=True)
    gender                                                            = messages.StringField(18, repeated=True)
    overall_survival                                                  = messages.IntegerField(19, repeated=True, variant=messages.Variant.INT32)
    overall_survival_lte                                              = messages.IntegerField(20, variant=messages.Variant.INT32)
    overall_survival_gte                                              = messages.IntegerField(21, variant=messages.Variant.INT32)
    
    program_name                                                      = messages.StringField(22, repeated=True)
    project_disease_type                                              = messages.StringField(23, repeated=True)
    project_short_name                                                = messages.StringField(24, repeated=True)
    protocol                                                          = messages.StringField(25, repeated=True)
    race                                                              = messages.StringField(26, repeated=True)
    summary_file_count                                                = messages.IntegerField(27, repeated=True, variant=messages.Variant.INT32)
    summary_file_count_lte                                            = messages.IntegerField(28, variant=messages.Variant.INT32)
    summary_file_count_gte                                            = messages.IntegerField(29, variant=messages.Variant.INT32)
    
    vital_status                                                      = messages.StringField(30, repeated=True)
    wbc_at_diagnosis                                                  = messages.FloatField(31, repeated=True)
    wbc_at_diagnosis_lte                                              = messages.FloatField(32)
    wbc_at_diagnosis_gte                                              = messages.FloatField(33)
    
    year_of_diagnosis                                                 = messages.IntegerField(34, repeated=True, variant=messages.Variant.INT32)
    year_of_diagnosis_lte                                             = messages.IntegerField(35, variant=messages.Variant.INT32)
    year_of_diagnosis_gte                                             = messages.IntegerField(36, variant=messages.Variant.INT32)
    
    year_of_last_follow_up                                            = messages.IntegerField(37, repeated=True, variant=messages.Variant.INT32)
    year_of_last_follow_up_lte                                        = messages.IntegerField(38, variant=messages.Variant.INT32)
    year_of_last_follow_up_gte                                        = messages.IntegerField(39, variant=messages.Variant.INT32)
    
    sample_barcode                                                    = messages.StringField(40, repeated=True)
    sample_gdc_id                                                     = messages.StringField(41, repeated=True)
    sample_type                                                       = messages.StringField(42, repeated=True)
    tumor_code                                                        = messages.StringField(43, repeated=True)
    
class MetadataItem(messages.Message):
    age_at_diagnosis                                                  = messages.IntegerField(1, variant=messages.Variant.INT32)
    case_barcode                                                      = messages.StringField(2)
    case_gdc_id                                                       = messages.StringField(3)
    days_to_birth                                                     = messages.IntegerField(4, variant=messages.Variant.INT32)
    days_to_death                                                     = messages.IntegerField(5, variant=messages.Variant.INT32)
    endpoint_type                                                     = messages.StringField(6)
    ethnicity                                                         = messages.StringField(7)
    event_free_survival                                               = messages.IntegerField(8, variant=messages.Variant.INT32)
    first_event                                                       = messages.StringField(9)
    gender                                                            = messages.StringField(10)
    overall_survival                                                  = messages.IntegerField(11, variant=messages.Variant.INT32)
    program_name                                                      = messages.StringField(12)
    project_disease_type                                              = messages.StringField(13)
    project_short_name                                                = messages.StringField(14)
    protocol                                                          = messages.StringField(15)
    race                                                              = messages.StringField(16)
    summary_file_count                                                = messages.IntegerField(17, variant=messages.Variant.INT32)
    vital_status                                                      = messages.StringField(18)
    wbc_at_diagnosis                                                  = messages.FloatField(19)
    year_of_diagnosis                                                 = messages.IntegerField(20, variant=messages.Variant.INT32)
    year_of_last_follow_up                                            = messages.IntegerField(21, variant=messages.Variant.INT32)
    sample_barcode                                                    = messages.StringField(22)
    sample_gdc_id                                                     = messages.StringField(23)
    sample_type                                                       = messages.StringField(24)
    tumor_code                                                        = messages.StringField(25)
    
shared_fields = ['case_barcode', 'endpoint_type', 'program_name', 'project_disease_type', 'project_short_name']