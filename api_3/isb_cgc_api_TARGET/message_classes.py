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
    
    days_to_last_followup                                             = messages.IntegerField(12, repeated=True, variant=messages.Variant.INT32)
    days_to_last_followup_lte                                         = messages.IntegerField(13, variant=messages.Variant.INT32)
    days_to_last_followup_gte                                         = messages.IntegerField(14, variant=messages.Variant.INT32)
    
    days_to_last_known_alive                                          = messages.IntegerField(15, repeated=True, variant=messages.Variant.INT32)
    days_to_last_known_alive_lte                                      = messages.IntegerField(16, variant=messages.Variant.INT32)
    days_to_last_known_alive_gte                                      = messages.IntegerField(17, variant=messages.Variant.INT32)
    
    disease_code                                                      = messages.StringField(18, repeated=True)
    endpoint_type                                                     = messages.StringField(19, repeated=True)
    ethnicity                                                         = messages.StringField(20, repeated=True)
    event_free_survival                                               = messages.IntegerField(21, repeated=True, variant=messages.Variant.INT32)
    event_free_survival_lte                                           = messages.IntegerField(22, variant=messages.Variant.INT32)
    event_free_survival_gte                                           = messages.IntegerField(23, variant=messages.Variant.INT32)
    
    first_event                                                       = messages.StringField(24, repeated=True)
    gender                                                            = messages.StringField(25, repeated=True)
    program_name                                                      = messages.StringField(29, repeated=True)
    project_short_name                                                = messages.StringField(30, repeated=True)
    protocol                                                          = messages.StringField(31, repeated=True)
    race                                                              = messages.StringField(32, repeated=True)
    summary_file_count                                                = messages.IntegerField(33, repeated=True, variant=messages.Variant.INT32)
    summary_file_count_lte                                            = messages.IntegerField(34, variant=messages.Variant.INT32)
    summary_file_count_gte                                            = messages.IntegerField(35, variant=messages.Variant.INT32)
    
    vital_status                                                      = messages.StringField(36, repeated=True)
    wbc_at_diagnosis                                                  = messages.FloatField(37, repeated=True)
    wbc_at_diagnosis_lte                                              = messages.FloatField(38)
    wbc_at_diagnosis_gte                                              = messages.FloatField(39)
    
    year_of_diagnosis                                                 = messages.IntegerField(40, repeated=True, variant=messages.Variant.INT32)
    year_of_diagnosis_lte                                             = messages.IntegerField(41, variant=messages.Variant.INT32)
    year_of_diagnosis_gte                                             = messages.IntegerField(42, variant=messages.Variant.INT32)
    
    year_of_last_follow_up                                            = messages.IntegerField(43, repeated=True, variant=messages.Variant.INT32)
    year_of_last_follow_up_lte                                        = messages.IntegerField(44, variant=messages.Variant.INT32)
    year_of_last_follow_up_gte                                        = messages.IntegerField(45, variant=messages.Variant.INT32)
    
    sample_barcode                                                    = messages.StringField(46, repeated=True)
    sample_gdc_id                                                     = messages.StringField(47, repeated=True)
    sample_type                                                       = messages.StringField(48, repeated=True)
    tumor_code                                                        = messages.StringField(49, repeated=True)
    
class MetadataItem(messages.Message):
    age_at_diagnosis                                                  = messages.IntegerField(1, variant=messages.Variant.INT32)
    case_barcode                                                      = messages.StringField(2)
    case_gdc_id                                                       = messages.StringField(3)
    days_to_birth                                                     = messages.IntegerField(4, variant=messages.Variant.INT32)
    days_to_death                                                     = messages.IntegerField(5, variant=messages.Variant.INT32)
    days_to_last_followup                                             = messages.IntegerField(6, variant=messages.Variant.INT32)
    days_to_last_known_alive                                          = messages.IntegerField(7, variant=messages.Variant.INT32)
    disease_code                                                      = messages.StringField(8)
    endpoint_type                                                     = messages.StringField(9)
    ethnicity                                                         = messages.StringField(10)
    event_free_survival                                               = messages.IntegerField(11, variant=messages.Variant.INT32)
    first_event                                                       = messages.StringField(12)
    gender                                                            = messages.StringField(13)
    program_name                                                      = messages.StringField(15)
    project_short_name                                                = messages.StringField(16)
    protocol                                                          = messages.StringField(17)
    race                                                              = messages.StringField(18)
    summary_file_count                                                = messages.IntegerField(19, variant=messages.Variant.INT32)
    vital_status                                                      = messages.StringField(20)
    wbc_at_diagnosis                                                  = messages.FloatField(21)
    year_of_diagnosis                                                 = messages.IntegerField(22, variant=messages.Variant.INT32)
    year_of_last_follow_up                                            = messages.IntegerField(23, variant=messages.Variant.INT32)
    sample_barcode                                                    = messages.StringField(24)
    sample_gdc_id                                                     = messages.StringField(25)
    sample_type                                                       = messages.StringField(26)
    tumor_code                                                        = messages.StringField(27)
    
shared_fields = ['case_barcode', 'disease_code', 'endpoint_type', 'program_name', 'project_short_name']
