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

from api_3.isb_cgc_api_TARGET.isb_cgc_api_helpers import ISB_CGC_TARGET_Endpoints
from api_3.isb_cgc_api_TARGET.message_classes import MetadataItem
from api_3.samples_get_helper import DataDetails, SamplesGetAPI

class SampleDetails(messages.Message):
    biospecimen_data = messages.MessageField(MetadataItem, 1)
    aliquots = messages.StringField(2, repeated=True)
    case_barcode = messages.StringField(3)
    case_gdc_id = messages.StringField(4)
    data_details = messages.MessageField(DataDetails, 5, repeated=True)
    data_details_count = messages.IntegerField(6, variant=messages.Variant.INT32)

@ISB_CGC_TARGET_Endpoints.api_class(resource_name='samples')
class TARGET_SamplesGetAPI(SamplesGetAPI):
    @endpoints.method(SamplesGetAPI.GET_RESOURCE, SampleDetails, path='target/samples/{sample_barcode}', http_method='GET')
    def get(self, request):
        """
        Given a sample barcode (of length 20-22, *eg* TARGET-51-PALFYG-01A), this endpoint returns
        all available "biospecimen" information about this sample,
        the associated case barcode, a list of associated aliquots,
        and a list of "data_details" blocks describing each of the data files associated with this sample
        """
        return super(TARGET_SamplesGetAPI, self).get(request, 'TARGET', SampleDetails, MetadataItem)
