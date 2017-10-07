"""

Copyright 2016, Institute for Systems Biology

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

from api_3.cohort_create_preview_helper import CohortsCreateHelper, CreatedCohort
from api_3.isb_cgc_api_CCLE.isb_cgc_api_helpers import ISB_CGC_CCLE_Endpoints
from api_3.isb_cgc_api_CCLE.message_classes import MetadataRangesItem

@ISB_CGC_CCLE_Endpoints.api_class(resource_name='cohorts')
class CCLE_CohortsCreateAPI(CohortsCreateHelper):
    POST_RESOURCE = endpoints.ResourceContainer(MetadataRangesItem, name=messages.StringField(2, required=True))

    @endpoints.method(POST_RESOURCE, CreatedCohort, path='ccle/cohorts/create', http_method='POST')
    def create(self, request):
        """
        Creates and saves a cohort. Takes a JSON object in the request body to use as the cohort's filters.
        Authentication is required.
        Returns information about the saved cohort, including the number of cases and the number
        of samples in that cohort.
        """
        self.program = 'CCLE'
        return super(CCLE_CohortsCreateAPI, self).create(request)
