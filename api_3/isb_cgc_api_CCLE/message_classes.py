from protorpc import messages

class MetadataRangesItem(messages.Message):
    case_barcode                                                      = messages.StringField(1, repeated=True)
    case_gdc_id                                                       = messages.StringField(2, repeated=True)
    disease_code                                                      = messages.StringField(3, repeated=True)
    endpoint_type                                                     = messages.StringField(4, repeated=True)
    gender                                                            = messages.StringField(5, repeated=True)
    histology                                                         = messages.StringField(6, repeated=True)
    hist_subtype                                                      = messages.StringField(7, repeated=True)
    program_name                                                      = messages.StringField(8, repeated=True)
    project_short_name                                                = messages.StringField(9, repeated=True)
    site_primary                                                      = messages.StringField(10, repeated=True)
    source                                                            = messages.StringField(11, repeated=True)
    summary_file_count                                                = messages.IntegerField(12, repeated=True, variant=messages.Variant.INT32)
    summary_file_count_lte                                            = messages.IntegerField(13, variant=messages.Variant.INT32)
    summary_file_count_gte                                            = messages.IntegerField(14, variant=messages.Variant.INT32)
    
    sample_barcode                                                    = messages.StringField(15, repeated=True)
    sample_gdc_id                                                     = messages.StringField(16, repeated=True)
    sample_type                                                       = messages.StringField(17, repeated=True)
    
class MetadataItem(messages.Message):
    case_barcode                                                      = messages.StringField(1)
    case_gdc_id                                                       = messages.StringField(2)
    disease_code                                                      = messages.StringField(3)
    endpoint_type                                                     = messages.StringField(4)
    gender                                                            = messages.StringField(5)
    histology                                                         = messages.StringField(6)
    hist_subtype                                                      = messages.StringField(7)
    program_name                                                      = messages.StringField(8)
    project_short_name                                                = messages.StringField(9)
    site_primary                                                      = messages.StringField(10)
    source                                                            = messages.StringField(11)
    summary_file_count                                                = messages.IntegerField(12, variant=messages.Variant.INT32)
    sample_barcode                                                    = messages.StringField(13)
    sample_gdc_id                                                     = messages.StringField(14)
    sample_type                                                       = messages.StringField(15)
    
shared_fields = ['case_barcode', 'disease_code', 'endpoint_type', 'program_name', 'project_short_name']