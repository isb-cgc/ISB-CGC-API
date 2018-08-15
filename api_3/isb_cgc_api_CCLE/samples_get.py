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
import endpoints
from protorpc import messages

from api_3.isb_cgc_api_CCLE.isb_cgc_api_helpers import ISB_CGC_CCLE_Endpoints
from api_3.isb_cgc_api_CCLE.message_classes import MetadataItem
from api_3.samples_get_helper import SamplesGetAPI, DataDetails


class SampleDetails(messages.Message):
    biospecimen_data = messages.MessageField(MetadataItem, 1)
    aliquots = messages.StringField(2, repeated=True)
    case_barcode = messages.StringField(3)
    case_gdc_id = messages.StringField(4)
    data_details = messages.MessageField(DataDetails, 5, repeated=True)
    data_details_count = messages.IntegerField(6, variant=messages.Variant.INT32)
    sample_barcode = messages.StringField(7)


class SampleSetDetails(messages.Message):
    samples = messages.MessageField(SampleDetails, 1, repeated=True)


@ISB_CGC_CCLE_Endpoints.api_class(resource_name='samples')
class CCLESamplesGetAPI(SamplesGetAPI):
    @endpoints.method(SamplesGetAPI.GET_RESOURCE, SampleDetails, path='ccle/samples/{sample_barcode}', http_method='GET')
    def get(self, request):
        """
        Given a sample barcode (*eg* CCLE-ACC-MESO-1), this endpoint returns
        the associated case barcode, a list of associated aliquots,
        and a list of "data_details" blocks describing each of the data files associated with this sample
        """
        return super(CCLESamplesGetAPI, self).get(request, 'CCLE', SampleDetails, MetadataItem)


    @endpoints.method(SamplesGetAPI.POST_RESOURCE, SampleSetDetails, path='ccle/samples', http_method='POST')
    def get_list(self, request):
        """
        Given a list of sample barcodes (of length 16, *eg* CCLE-ACC-MESO-1), this endpoint returns
        the associated case barcode, a list of associated aliquots,
        and a list of "data_details" blocks describing each of the data files associated with this sample
        """
        return super(CCLESamplesGetAPI, self).get_list(request, 'CCLE', SampleSetDetails, SampleDetails, MetadataItem)
