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
 
from api_3.isb_cgc_api.cohorts_delete import CohortsDeleteAPI
from api_3.isb_cgc_api.cohorts_get import CohortsGetAPI
from api_3.isb_cgc_api.cohorts_list import CohortsListAPI
from api_3.isb_cgc_api.cohorts_cloudstoragefilepaths import CohortsCloudStorageFilePathsAPI
 
from api_3.isb_cgc_api_TCGA.cohorts_preview import TCGA_CohortsPreviewAPI
from api_3.isb_cgc_api_TCGA.cohorts_create import TCGA_CohortsCreateAPI
from api_3.isb_cgc_api_TCGA.patients_get import TCGA_CasesGetAPI
from api_3.isb_cgc_api_TCGA.patients_annotations import TCGA_CasesAnnotationAPI
from api_3.isb_cgc_api_TCGA.samples_get import TCGA_SamplesGetAPI
from api_3.isb_cgc_api_TCGA.samples_cloudstoragefilepaths import TCGA_SamplesCloudStorageFilePathsAPI
from api_3.isb_cgc_api_TCGA.samples_annotations import TCGA_SamplesAnnotationAPI
from api_3.isb_cgc_api_TCGA.aliquots_annotations import TCGA_AliquotsAnnotationAPI
from api_3.isb_cgc_api_TCGA.users_get import TCGA_UserGetAPI
 
from api_3.isb_cgc_api_TARGET.cohorts_preview import TARGET_CohortsPreviewAPI
from api_3.isb_cgc_api_TARGET.cohorts_create import TARGET_CohortsCreateAPI
from api_3.isb_cgc_api_TARGET.patients_get import TARGET_CasesGetAPI
from api_3.isb_cgc_api_TARGET.samples_get import TARGET_SamplesGetAPI
from api_3.isb_cgc_api_TARGET.samples_cloudstoragefilepaths import TARGET_SamplesCloudStorageFilePathsAPI
from api_3.isb_cgc_api_TARGET.users_get import TARGET_UserGetAPI
 
from api_3.isb_cgc_api_CCLE.cohorts_preview import CCLE_CohortsPreviewAPI
from api_3.isb_cgc_api_CCLE.cohorts_create import CCLE_CohortsCreateAPI
from api_3.isb_cgc_api_CCLE.patients_get import CCLE_CasesGetAPI
from api_3.isb_cgc_api_CCLE.samples_get import CCLE_SamplesGetAPI
from api_3.isb_cgc_api_CCLE.samples_cloudstoragefilepaths import CCLE_SamplesCloudStorageFilePathsAPI
 
package = 'isb-cgc-api'
 
APPLICATION = endpoints.api_server([
    CohortsDeleteAPI,
    CohortsGetAPI,
    CohortsListAPI,
    CohortsCloudStorageFilePathsAPI,
 
    TCGA_CohortsPreviewAPI,
    TCGA_CohortsCreateAPI,
    TCGA_CasesGetAPI,
    TCGA_CasesAnnotationAPI,
    TCGA_SamplesGetAPI,
    TCGA_SamplesCloudStorageFilePathsAPI,
    TCGA_SamplesAnnotationAPI,
    TCGA_AliquotsAnnotationAPI,
    TCGA_UserGetAPI,
         
    TARGET_CohortsPreviewAPI,
    TARGET_CohortsCreateAPI,
    TARGET_CasesGetAPI,
    TARGET_SamplesGetAPI,
    TARGET_SamplesCloudStorageFilePathsAPI,
    TARGET_UserGetAPI,
         
    CCLE_CohortsPreviewAPI,
    CCLE_CohortsCreateAPI,
    CCLE_CasesGetAPI,
    CCLE_SamplesGetAPI,
    CCLE_SamplesCloudStorageFilePathsAPI
])
