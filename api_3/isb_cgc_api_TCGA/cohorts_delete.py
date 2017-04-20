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

from api_3.cohorts_delete_helper import CohortsDeleteHelper, ReturnJSON
from api_3.isb_cgc_api_TCGA.isb_cgc_api_helpers import ISB_CGC_TCGA_Endpoints

@ISB_CGC_TCGA_Endpoints.api_class(resource_name='cohorts')
class TCGA_CohortsDeleteAPI(CohortsDeleteHelper):
    @endpoints.method(CohortsDeleteHelper.DELETE_RESOURCE, ReturnJSON, http_method='DELETE', path='cohorts/{cohort_id}')
    def delete(self, request):
        """
        Deletes a cohort. User must have owner permissions on the cohort.
        """
        return super(TCGA_CohortsDeleteAPI, self).delete(request)
