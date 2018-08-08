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
from api_3.isb_cgc_api_TARGET.message_classes import BiospecimenMetadataItem
from api_3.samples_get_helper import SamplesGetAPI, SampleDetails, SampleSetDetails


@ISB_CGC_TARGET_Endpoints.api_class(resource_name='samples')
class TARGETSamplesGetAPI(SamplesGetAPI):
    @endpoints.method(SamplesGetAPI.GET_RESOURCE, SampleDetails, path='target/samples/{sample_barcode}', http_method='GET')
    def get(self, request):
        """
        Given a sample barcode (of length 20-22, *eg* TARGET-51-PALFYG-01A), this endpoint returns
        all available "biospecimen" information about this sample,
        the associated case barcode, a list of associated aliquots,
        and a list of "data_details" blocks describing each of the data files associated with this sample
        """
        return super(TARGETSamplesGetAPI, self).get(request, 'TARGET', SampleDetails, BiospecimenMetadataItem)

    @endpoints.method(SamplesGetAPI.POST_RESOURCE, SampleSetDetails, path='target/samples', http_method='POST')
    def get_list(self, request):
        """
        Given a list of sample barcodes (of length 16, *eg* TARGET-B9-7268-01A), this endpoint returns
        all available "biospecimen" information about this sample,
        the associated case barcode, a list of associated aliquots,
        and a list of "data_details" blocks describing each of the data files associated with this sample
        """
        return super(TARGETSamplesGetAPI, self).get_list(request, 'TARGET', SampleSetDetails, SampleDetails, BiospecimenMetadataItem)
