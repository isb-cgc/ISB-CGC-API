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

from api_3.isb_cgc_api_CCLE.isb_cgc_api_helpers import ISB_CGC_CCLE_Endpoints
from api_3.cohort_get_list_helper import CohortDetails, CohortsGetHelper

@ISB_CGC_CCLE_Endpoints.api_class(resource_name='cohorts')
class CohortsGetAPI(CohortsGetHelper):
    @endpoints.method(CohortsGetHelper.GET_RESOURCE, CohortDetails, http_method='GET', path='cohorts/{cohort_id}')
    def get(self, request):
        """
        Returns information about a specific cohort the user has READER or OWNER permission on
        when given a cohort ID. Authentication is required.
        """
        return super(CohortsGetAPI, self).get(request)
