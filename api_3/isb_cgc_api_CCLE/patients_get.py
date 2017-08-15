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

from api_3.patients_get_helper import CasesGetHelper
from api_3.isb_cgc_api_CCLE.message_classes import MetadataItem
from api_3.isb_cgc_api_CCLE.isb_cgc_api_helpers import ISB_CGC_CCLE_Endpoints

class CaseDetails(messages.Message):
    clinical_data = messages.MessageField(MetadataItem, 1)
    samples = messages.StringField(2, repeated=True)
    aliquots = messages.StringField(3, repeated=True)

@ISB_CGC_CCLE_Endpoints.api_class(resource_name='cases')
class CCLE_CasesGetAPI(CasesGetHelper):
    @endpoints.method(CasesGetHelper.GET_RESOURCE, CaseDetails, path='ccle/cases/{case_barcode}', http_method='GET')
    def get(self, request):
        """
        Returns information about a specific case,
        including a list of samples and aliquots derived from this case.
        Takes a case barcode (*eg* ACC-MESO-1) as a required parameter.
        User does not need to be authenticated.
        """
        return super(CCLE_CasesGetAPI, self).get(request, CaseDetails, MetadataItem, 'CCLE')
