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
from api_3.isb_cgc_api.files_get_file_paths import FilesGetPath
from api_3.isb_cgc_api.cohort_file_manifest import CohortFileManifestAPI
 
from api_3.isb_cgc_api_TCGA.cohorts_preview import TCGACohortsPreviewAPI
from api_3.isb_cgc_api_TCGA.cohorts_create import TCGACohortsCreateAPI
from api_3.isb_cgc_api_TCGA.patients_get import TCGACasesGetAPI
from api_3.isb_cgc_api_TCGA.samples_get import TCGASamplesGetAPI
from api_3.isb_cgc_api_TCGA.samples_cloudstoragefilepaths import TCGASamplesCloudStorageFilePathsAPI
from api_3.isb_cgc_api_TCGA.users_get import TCGAUserGetAPI
 
from api_3.isb_cgc_api_TARGET.cohorts_preview import TARGETCohortsPreviewAPI
from api_3.isb_cgc_api_TARGET.cohorts_create import TARGETCohortsCreateAPI
from api_3.isb_cgc_api_TARGET.patients_get import TARGETCasesGetAPI
from api_3.isb_cgc_api_TARGET.samples_get import TARGETSamplesGetAPI
from api_3.isb_cgc_api_TARGET.samples_cloudstoragefilepaths import TARGETSamplesCloudStorageFilePathsAPI
from api_3.isb_cgc_api_TARGET.users_get import TARGETUserGetAPI
 
from api_3.isb_cgc_api_CCLE.cohorts_preview import CCLECohortsPreviewAPI
from api_3.isb_cgc_api_CCLE.cohorts_create import CCLECohortsCreateAPI
from api_3.isb_cgc_api_CCLE.patients_get import CCLECasesGetAPI
from api_3.isb_cgc_api_CCLE.samples_get import CCLESamplesGetAPI
from api_3.isb_cgc_api_CCLE.samples_cloudstoragefilepaths import CCLESamplesCloudStorageFilePathsAPI
 
package = 'isb-cgc-api'
 
APPLICATION = endpoints.api_server([
    CohortsDeleteAPI,
    CohortsGetAPI,
    CohortsListAPI,
    CohortsCloudStorageFilePathsAPI,
    CohortFileManifestAPI,
    FilesGetPath,
 
    TCGACohortsPreviewAPI,
    TCGACohortsCreateAPI,
    TCGACasesGetAPI,
    TCGASamplesGetAPI,
    TCGASamplesCloudStorageFilePathsAPI,
    TCGAUserGetAPI,
         
    TARGETCohortsPreviewAPI,
    TARGETCohortsCreateAPI,
    TARGETCasesGetAPI,
    TARGETSamplesGetAPI,
    TARGETSamplesCloudStorageFilePathsAPI,
    TARGETUserGetAPI,
         
    CCLECohortsPreviewAPI,
    CCLECohortsCreateAPI,
    CCLECasesGetAPI,
    CCLESamplesGetAPI,
    CCLESamplesCloudStorageFilePathsAPI
])
