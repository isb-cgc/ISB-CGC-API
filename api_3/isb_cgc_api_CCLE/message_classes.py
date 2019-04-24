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
    case_barcode                                                      = messages.StringField(1, repeated=True)
    case_gdc_id                                                       = messages.StringField(2, repeated=True)
    gender                                                            = messages.StringField(3, repeated=True)
    histology                                                         = messages.StringField(4, repeated=True)
    hist_subtype                                                      = messages.StringField(5, repeated=True)
    site_primary                                                      = messages.StringField(6, repeated=True)
    source                                                            = messages.StringField(7, repeated=True)
    summary_file_count                                                = messages.IntegerField(8, repeated=True, variant=messages.Variant.INT32)
    summary_file_count_lte                                            = messages.IntegerField(9, variant=messages.Variant.INT32)
    summary_file_count_gte                                            = messages.IntegerField(10, variant=messages.Variant.INT32)
    
    
class ClinicalMetadataItem(messages.Message):
    case_barcode                                                      = messages.StringField(1)
    case_gdc_id                                                       = messages.StringField(2)
    gender                                                            = messages.StringField(3)
    histology                                                         = messages.StringField(4)
    hist_subtype                                                      = messages.StringField(5)
    site_primary                                                      = messages.StringField(6)
    source                                                            = messages.StringField(7)
    summary_file_count                                                = messages.IntegerField(8, variant=messages.Variant.INT32)
    
class BiospecimenMetadataRangesItem(messages.Message):
    case_barcode                                                      = messages.StringField(1, repeated=True)
    case_gdc_id                                                       = messages.StringField(2, repeated=True)
    sample_barcode                                                    = messages.StringField(3, repeated=True)
    sample_gdc_id                                                     = messages.StringField(4, repeated=True)
    sample_type                                                       = messages.StringField(5, repeated=True)
    
class BiospecimenMetadataItem(messages.Message):
    case_barcode                                                      = messages.StringField(1)
    case_gdc_id                                                       = messages.StringField(2)
    sample_barcode                                                    = messages.StringField(3)
    sample_gdc_id                                                     = messages.StringField(4)
    sample_type                                                       = messages.StringField(5)
    
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
    
class Data_HG19MetadataItem(messages.Message):
    access                                                            = messages.StringField(1)
    case_barcode                                                      = messages.StringField(5)
    case_gdc_id                                                       = messages.StringField(6)
    center_code                                                       = messages.StringField(7)
    center_name                                                       = messages.StringField(8)
    center_type                                                       = messages.StringField(9)
    data_category                                                     = messages.StringField(10)
    data_format                                                       = messages.StringField(11)
    data_type                                                         = messages.StringField(12)
    experimental_strategy                                             = messages.StringField(13)
    file_name_key                                                         = messages.StringField(14)
    index_file_name_key                                                   = messages.StringField(17)
    platform                                                          = messages.StringField(18)
    sample_barcode                                                    = messages.StringField(19)
    sample_gdc_id                                                     = messages.StringField(20)
    
class MetadataRangesItem(messages.Message):
    Common = messages.MessageField(CommonMetadataRangesItem, 1)
    Clinical = messages.MessageField(ClinicalMetadataRangesItem, 2)
    Biospecimen = messages.MessageField(BiospecimenMetadataRangesItem, 3)
    data_HG19_r14 = messages.MessageField(Data_HG19MetadataRangesItem, 4)

class MetadataItem(messages.Message):
    Common = messages.MessageField(CommonMetadataItem, 1)
    Clinical = messages.MessageField(ClinicalMetadataItem, 2)
    Biospecimen = messages.MessageField(BiospecimenMetadataItem, 3)
    data_HG19_r14 = messages.MessageField(Data_HG19MetadataItem, 4)

