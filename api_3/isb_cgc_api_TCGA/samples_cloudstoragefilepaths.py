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

from api_3.isb_cgc_api_TCGA.isb_cgc_api_helpers import ISB_CGC_TCGA_Endpoints
from api_3.cloudstoragefilepaths_helper import GCSFilePathList, SamplesCloudStorageFilePathsHelper

@ISB_CGC_TCGA_Endpoints.api_class(resource_name='samples')
class SamplesCloudStorageFilePathsAPI(SamplesCloudStorageFilePathsHelper):

    @endpoints.method(SamplesCloudStorageFilePathsHelper.GET_RESOURCE, GCSFilePathList,
                      path='samples/{sample_barcode}/cloud_storage_file_paths', http_method='GET')
    def cloud_storage_file_paths(self, request):
        """
        Takes a sample barcode as a required parameter and
        returns cloud storage paths to files associated with that sample.
        """
        super(SamplesCloudStorageFilePathsAPI, self).cloud_storage_file_paths(request)
