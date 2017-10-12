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
    gender                                                            = messages.StringField(2, repeated=True)
    histology                                                         = messages.StringField(3, repeated=True)
    hist_subtype                                                      = messages.StringField(4, repeated=True)
    site_primary                                                      = messages.StringField(5, repeated=True)
    source                                                            = messages.StringField(6, repeated=True)
    summary_file_count                                                = messages.IntegerField(7, repeated=True, variant=messages.Variant.INT32)
    summary_file_count_lte                                            = messages.IntegerField(8, variant=messages.Variant.INT32)
    summary_file_count_gte                                            = messages.IntegerField(9, variant=messages.Variant.INT32)
    
    
class ClinicalMetadataItem(messages.Message):
    case_barcode                                                      = messages.StringField(1)
    gender                                                            = messages.StringField(2)
    histology                                                         = messages.StringField(3)
    hist_subtype                                                      = messages.StringField(4)
    site_primary                                                      = messages.StringField(5)
    source                                                            = messages.StringField(6)
    summary_file_count                                                = messages.IntegerField(7, variant=messages.Variant.INT32)
    
class BiospecimenMetadataRangesItem(messages.Message):
    case_barcode                                                      = messages.StringField(1, repeated=True)
    sample_barcode                                                    = messages.StringField(2, repeated=True)
    sample_type                                                       = messages.StringField(3, repeated=True)
    
class BiospecimenMetadataItem(messages.Message):
    case_barcode                                                      = messages.StringField(1)
    sample_barcode                                                    = messages.StringField(2)
    sample_type                                                       = messages.StringField(3)
    
class Data_HG19MetadataRangesItem(messages.Message):
    access                                                            = messages.StringField(1, repeated=True)
    aliquot_barcode                                                   = messages.StringField(2, repeated=True)
    analysis_workflow_type                                            = messages.StringField(3, repeated=True)
    case_barcode                                                      = messages.StringField(4, repeated=True)
    center_code                                                       = messages.StringField(5, repeated=True)
    center_name                                                       = messages.StringField(6, repeated=True)
    center_type                                                       = messages.StringField(7, repeated=True)
    data_category                                                     = messages.StringField(8, repeated=True)
    data_format                                                       = messages.StringField(9, repeated=True)
    data_type                                                         = messages.StringField(10, repeated=True)
    experimental_strategy                                             = messages.StringField(11, repeated=True)
    file_name                                                         = messages.StringField(12, repeated=True)
    file_state                                                        = messages.StringField(13, repeated=True)
    file_uploaded                                                     = messages.StringField(14, repeated=True)
    index_file_name                                                   = messages.StringField(15, repeated=True)
    platform                                                          = messages.StringField(16, repeated=True)
    sample_barcode                                                    = messages.StringField(17, repeated=True)
    sample_type                                                       = messages.StringField(18, repeated=True)
    species                                                           = messages.StringField(19, repeated=True)
    
class Data_HG19MetadataItem(messages.Message):
    access                                                            = messages.StringField(1)
    aliquot_barcode                                                   = messages.StringField(2)
    analysis_workflow_type                                            = messages.StringField(3)
    case_barcode                                                      = messages.StringField(4)
    center_code                                                       = messages.StringField(5)
    center_name                                                       = messages.StringField(6)
    center_type                                                       = messages.StringField(7)
    data_category                                                     = messages.StringField(8)
    data_format                                                       = messages.StringField(9)
    data_type                                                         = messages.StringField(10)
    experimental_strategy                                             = messages.StringField(11)
    file_name                                                         = messages.StringField(12)
    file_state                                                        = messages.StringField(13)
    file_uploaded                                                     = messages.StringField(14)
    index_file_name                                                   = messages.StringField(15)
    platform                                                          = messages.StringField(16)
    sample_barcode                                                    = messages.StringField(17)
    sample_type                                                       = messages.StringField(18)
    species                                                           = messages.StringField(19)
    
class MetadataRangesItem(messages.Message):
    Common = messages.MessageField(CommonMetadataRangesItem, 1)
    Clinical = messages.MessageField(ClinicalMetadataRangesItem, 2)
    Biospecimen = messages.MessageField(BiospecimenMetadataRangesItem, 3)
    Data_HG19 = messages.MessageField(Data_HG19MetadataRangesItem, 4)

class MetadataItem(messages.Message):
    Common = messages.MessageField(CommonMetadataItem, 1)
    Clinical = messages.MessageField(ClinicalMetadataItem, 2)
    Biospecimen = messages.MessageField(BiospecimenMetadataItem, 3)
    Data_HG19 = messages.MessageField(Data_HG19MetadataItem, 4)

