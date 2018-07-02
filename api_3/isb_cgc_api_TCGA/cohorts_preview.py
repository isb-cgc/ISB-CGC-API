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

from api_3.cohort_create_preview_helper import CohortsPreviewHelper
from api_3.isb_cgc_api_TCGA.isb_cgc_api_helpers import ISB_CGC_TCGA_Endpoints
from message_classes import MetadataRangesItem

@ISB_CGC_TCGA_Endpoints.api_class(resource_name='cohorts')
class TCGA_CohortsPreviewAPI(CohortsPreviewHelper):

    POST_RESOURCE = endpoints.ResourceContainer(MetadataRangesItem, fields=messages.StringField(3))

    @endpoints.method(POST_RESOURCE, CohortsPreviewHelper.CohortCasesSamplesList, path='tcga/cohorts/preview', http_method='POST')
    def preview(self, request):
        """
        Takes a JSON object of filters in the request body and returns a "preview" of the cohort that would
        result from passing a similar request to the cohort **save** endpoint.  This preview consists of
        two lists: the lists of case barcodes, and the list of sample barcodes.
        Authentication is not required.
        """
        self.program = 'TCGA'
        return super(TCGA_CohortsPreviewAPI, self).preview(request)
