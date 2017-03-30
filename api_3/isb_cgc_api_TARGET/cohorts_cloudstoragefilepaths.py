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

from api_3.isb_cgc_api_TARGET.isb_cgc_api_helpers import ISB_CGC_TARGET_Endpoints
from api_3.cloudstoragefilepaths_helper import GCSFilePathList, CohortsCloudStorageFilePathsHelper

@ISB_CGC_TARGET_Endpoints.api_class(resource_name='cohorts')
class CohortsCloudStorageFilePathsAPI(CohortsCloudStorageFilePathsHelper):
    @endpoints.method(CohortsCloudStorageFilePathsHelper.GET_RESOURCE, GCSFilePathList,  http_method='GET',
                      path='cohorts/{cohort_id}/cloud_storage_file_paths')
    def cloud_storage_file_paths(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        super(CohortsCloudStorageFilePathsAPI, self).cloud_storage_file_paths(request)
