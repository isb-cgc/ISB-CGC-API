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

from api_3.feature_access import FeatureAccessEndpoints
from api_3.single_feature_access import SingleFeatureDataAccess
from api_3.data_access import FeatureDataEndpoints

from api_3.Cohort import Cohort_Endpoints

from api_3.metadata import Meta_Endpoints, Meta_Endpoints_v2
from api_3.pairwise_api import Pairwise_Endpoints
from api_3.seqpeek_view_api import SeqPeekViewDataAccessAPI
from api_3.isb_cgc_api.cohorts_list import CohortsListAPI
from api_3.isb_cgc_api.cohorts_preview import CohortsPreviewAPI
from api_3.isb_cgc_api.cohorts_get import CohortsGetAPI
from api_3.isb_cgc_api.cohorts_delete import CohortsDeleteAPI
from api_3.isb_cgc_api.cohorts_create import CohortsCreateAPI
from api_3.isb_cgc_api.cohorts_cloudstoragefilepaths import CohortsCloudStorageFilePathsAPI
from api_3.isb_cgc_api.patients_get import PatientsGetAPI
from api_3.isb_cgc_api.patients_annotations import PatientsAnnotationAPI
from api_3.isb_cgc_api.samples_get import SamplesGetAPI
from api_3.isb_cgc_api.samples_cloudstoragefilepaths import SamplesCloudStorageFilePathsAPI
from api_3.isb_cgc_api.samples_annotations import SamplesAnnotationAPI
from api_3.isb_cgc_api.aliquots_annotations import AliquotsAnnotationAPI
from api_3.isb_cgc_api.users_get import UserGetAPI


package = 'isb-cgc-api'


APPLICATION = endpoints.api_server([
    Cohort_Endpoints,

    FeatureAccessEndpoints,
    Meta_Endpoints,
    Meta_Endpoints_v2,
    FeatureDataEndpoints,
    SingleFeatureDataAccess,
    Pairwise_Endpoints,
    SeqPeekViewDataAccessAPI,

    CohortsListAPI,
    CohortsPreviewAPI,
    CohortsGetAPI,
    CohortsDeleteAPI,
    CohortsCreateAPI,
    CohortsCloudStorageFilePathsAPI,
    PatientsGetAPI,
    PatientsAnnotationAPI,
    SamplesGetAPI,
    SamplesCloudStorageFilePathsAPI,
    SamplesAnnotationAPI,
    AliquotsAnnotationAPI,
    UserGetAPI,
])

