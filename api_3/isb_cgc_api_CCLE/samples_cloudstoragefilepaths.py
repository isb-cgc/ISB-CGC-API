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
from api_3.cloudstoragefilepaths_helper import GCSFilePathList, SamplesCloudStorageFilePathsHelper

@ISB_CGC_CCLE_Endpoints.api_class(resource_name='samples')
class CCLE_SamplesCloudStorageFilePathsAPI(SamplesCloudStorageFilePathsHelper):

    @endpoints.method(SamplesCloudStorageFilePathsHelper.GET_RESOURCE, GCSFilePathList,
                      path='ccle/samples/{sample_barcode}/cloud_storage_file_paths', http_method='GET')
    def cloud_storage_file_paths(self, request):
        """
        Takes a sample barcode as a required parameter and
        returns cloud storage paths to files associated with that sample.
        """
        return super(CCLE_SamplesCloudStorageFilePathsAPI, self).cloud_storage_file_paths(request, 'CCLE')
