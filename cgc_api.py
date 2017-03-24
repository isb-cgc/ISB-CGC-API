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

from api_3.isb_cgc_api_TCGA.cohorts_list import  CohortsListAPI as TCGA_CohortsListAPI
from api_3.isb_cgc_api_TCGA.cohorts_preview import  CohortsPreviewAPI as TCGA_CohortsPreviewAPI
from api_3.isb_cgc_api_TCGA.cohorts_get import  CohortsGetAPI as TCGA_CohortsGetAPI
from api_3.isb_cgc_api_TCGA.cohorts_delete import  CohortsDeleteAPI as TCGA_CohortsDeleteAPI
from api_3.isb_cgc_api_TCGA.cohorts_create import  CohortsCreateAPI as TCGA_CohortsCreateAPI
from api_3.isb_cgc_api_TCGA.cohorts_cloudstoragefilepaths import  CohortsCloudStorageFilePathsAPI as TCGA_CohortsCloudStorageFilePathsAPI
from api_3.isb_cgc_api_TCGA.patients_get import  PatientsGetAPI as TCGA_PatientsGetAPI
from api_3.isb_cgc_api_TCGA.patients_annotations import  PatientsAnnotationAPI as TCGA_PatientsAnnotationAPI
from api_3.isb_cgc_api_TCGA.samples_get import  SamplesGetAPI as TCGA_SamplesGetAPI
from api_3.isb_cgc_api_TCGA.samples_cloudstoragefilepaths import  SamplesCloudStorageFilePathsAPI as TCGA_SamplesCloudStorageFilePathsAPI
from api_3.isb_cgc_api_TCGA.samples_annotations import  SamplesAnnotationAPI as TCGA_SamplesAnnotationAPI
from api_3.isb_cgc_api_TCGA.aliquots_annotations import  AliquotsAnnotationAPI as TCGA_AliquotsAnnotationAPI
from api_3.isb_cgc_api_TCGA.users_get import  UserGetAPI as TCGA_UserGetAPI

from api_3.isb_cgc_api_TARGET.cohorts_list import  CohortsListAPI as TARGET_CohortsListAPI
from api_3.isb_cgc_api_TARGET.cohorts_preview import  CohortsPreviewAPI as TARGET_CohortsPreviewAPI
from api_3.isb_cgc_api_TARGET.cohorts_get import  CohortsGetAPI as TARGET_CohortsGetAPI
from api_3.isb_cgc_api_TARGET.cohorts_delete import  CohortsDeleteAPI as TARGET_CohortsDeleteAPI
from api_3.isb_cgc_api_TARGET.cohorts_create import  CohortsCreateAPI as TARGET_CohortsCreateAPI
from api_3.isb_cgc_api_TARGET.cohorts_cloudstoragefilepaths import  CohortsCloudStorageFilePathsAPI as TARGET_CohortsCloudStorageFilePathsAPI
from api_3.isb_cgc_api_TARGET.patients_get import  PatientsGetAPI as TARGET_PatientsGetAPI
from api_3.isb_cgc_api_TARGET.samples_get import  SamplesGetAPI as TARGET_SamplesGetAPI
from api_3.isb_cgc_api_TARGET.samples_cloudstoragefilepaths import  SamplesCloudStorageFilePathsAPI as TARGET_SamplesCloudStorageFilePathsAPI
from api_3.isb_cgc_api_TARGET.users_get import  UserGetAPI as TARGET_UserGetAPI

from api_3.isb_cgc_api_CCLE.cohorts_list import  CohortsListAPI as CCLE_CohortsListAPI
from api_3.isb_cgc_api_CCLE.cohorts_preview import  CohortsPreviewAPI as CCLE_CohortsPreviewAPI
from api_3.isb_cgc_api_CCLE.cohorts_get import  CohortsGetAPI as CCLE_CohortsGetAPI
from api_3.isb_cgc_api_CCLE.cohorts_delete import  CohortsDeleteAPI as CCLE_CohortsDeleteAPI
from api_3.isb_cgc_api_CCLE.cohorts_create import  CohortsCreateAPI as CCLE_CohortsCreateAPI
from api_3.isb_cgc_api_CCLE.cohorts_cloudstoragefilepaths import  CohortsCloudStorageFilePathsAPI as CCLE_CohortsCloudStorageFilePathsAPI
from api_3.isb_cgc_api_CCLE.patients_get import  PatientsGetAPI as CCLE_PatientsGetAPI
from api_3.isb_cgc_api_CCLE.samples_get import  SamplesGetAPI as CCLE_SamplesGetAPI
from api_3.isb_cgc_api_CCLE.samples_cloudstoragefilepaths import  SamplesCloudStorageFilePathsAPI as CCLE_SamplesCloudStorageFilePathsAPI
from api_3.isb_cgc_api_CCLE.users_get import  UserGetAPI as CCLE_UserGetAPI

package = 'isb-cgc-api'

APPLICATION = endpoints.api_server([
    TCGA_CohortsListAPI,
    TCGA_CohortsPreviewAPI,
    TCGA_CohortsGetAPI,
    TCGA_CohortsDeleteAPI,
    TCGA_CohortsCreateAPI,
    TCGA_CohortsCloudStorageFilePathsAPI,
    TCGA_PatientsGetAPI,
    TCGA_PatientsAnnotationAPI,
    TCGA_SamplesGetAPI,
    TCGA_SamplesCloudStorageFilePathsAPI,
    TCGA_SamplesAnnotationAPI,
    TCGA_AliquotsAnnotationAPI,
    TCGA_UserGetAPI,
        
    TARGET_CohortsListAPI,
    TARGET_CohortsPreviewAPI,
    TARGET_CohortsGetAPI,
    TARGET_CohortsDeleteAPI,
    TARGET_CohortsCreateAPI,
    TARGET_CohortsCloudStorageFilePathsAPI,
    TARGET_PatientsGetAPI,
    TARGET_SamplesGetAPI,
    TARGET_SamplesCloudStorageFilePathsAPI,
    TARGET_UserGetAPI,
        
    CCLE_CohortsListAPI,
    CCLE_CohortsPreviewAPI,
    CCLE_CohortsGetAPI,
    CCLE_CohortsDeleteAPI,
    CCLE_CohortsCreateAPI,
    CCLE_CohortsCloudStorageFilePathsAPI,
    CCLE_PatientsGetAPI,
    CCLE_SamplesGetAPI,
    CCLE_SamplesCloudStorageFilePathsAPI,
    CCLE_UserGetAPI
])

