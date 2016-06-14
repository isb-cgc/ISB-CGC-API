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

from api.feature_access import FeatureAccessEndpoints           # class FeatureAccessEndpoints(remote.Service) decorated with @FeatureAccessEndpointsAPI.api_class which is defined as FeatureAccessEndpointsAPI = endpoints_api(name='feature_type_api', ...)

from api.single_feature_access import SingleFeatureDataAccess   # class SingleFeatureDataAccess(remote.Service): decorated with @FeatureDataEndpointsAPI.api_class which is defined as FeatureAccessEndpointsAPI = endpoints_api(name='feature_type_api', ...)
from api.data_access import FeatureDataEndpoints                # class FeatureDataEndpoints(remote.Service): decorated with @FeatureDataEndpointsAPI.api_class which is defined as FeatureAccessEndpointsAPI = endpoints_api(name='feature_type_api', ...)

from api.Cohort import Cohort_Endpoints_API                     # class Cohort_Endpoints_API(remote.Service): decorated with @Cohort_Endpoints.api_class which is defined as Cohort_Endpoints = endpoints.api(name='cohort_api',..)
from api.cohort_api.preview_cohort import PreviewCohort
from api.cohort_api.cohorts_list import CohortsList
from api.cohort_api.cohort_patients_samples_list import CohortsPatientsSamplesList
from api.cohort_api.patient_details import PatientDetails
from api.cohort_api.sample_details import SampleDetails
from api.cohort_api.datafilenamekey_list import DataFileNameKeyList
from api.cohort_api.save_cohort import SaveCohort
from api.cohort_api.delete_cohort import DeleteCohort
# from api.cohort_api.cohort_helpers import Cohort_Endpoints2                       # endpoints.api(name='cohort_api', ...) @Cohort_Endpoints.api_class

from api.isb_cgc_api.cohorts_list import CohortsListAPI
from api.isb_cgc_api.cohorts_preview import CohortsPreviewAPI
from api.isb_cgc_api.cohorts_get import CohortsGetAPI
from api.isb_cgc_api.cohorts_delete import CohortsDeleteAPI
from api.isb_cgc_api.cohorts_create import CohortsCreateAPI
from api.isb_cgc_api.cohorts_datafilenamekeys import CohortsDatafilenamekeysAPI
from api.isb_cgc_api.cohorts_googlegenomics import CohortsGoogleGenomicssAPI
from api.isb_cgc_api.participants_get import ParticipantsGetAPI
from api.isb_cgc_api.samples_get import SamplesGetAPI
from api.isb_cgc_api.samples_datafilenamekeys import SamplesDatafilenamekeysAPI
from api.isb_cgc_api.samples_googlegenomics import SamplesGoogleGenomicsAPI

from api.metadata import Meta_Endpoints, Meta_Endpoints_v2      # endpoints.api(name='meta_api', ...) @Meta_Endpoints.api_class
from api.pairwise_api import Pairwise_Endpoints                 # endpoints.api(name='pairwise',...) @Pairwise_Endpoints.api_class
from api.seqpeek_view_api import SeqPeekViewDataAccessAPI       # class SeqPeekViewDataAccessAPI(remote.Service): decprated with @SeqPeekDataEndpointsAPI.api_class which is defined as SeqPeekDataEndpointsAPI = endpoints_api(name='seqpeek_data_api', ...)
# from api.users import User_Endpoints

package = 'isb-cgc-api'


APPLICATION = endpoints.api_server([
    Cohort_Endpoints_API,  # original

    PreviewCohort,
    CohortsList,
    CohortsPatientsSamplesList,
    PatientDetails,
    SampleDetails,
    DataFileNameKeyList,
    SaveCohort,
    DeleteCohort,

    CohortsListAPI,
    CohortsPreviewAPI,
    CohortsGetAPI,
    CohortsDeleteAPI,
    CohortsCreateAPI,
    CohortsDatafilenamekeysAPI,
    CohortsGoogleGenomicssAPI,
    ParticipantsGetAPI,
    SamplesGetAPI,
    SamplesDatafilenamekeysAPI,
    SamplesGoogleGenomicsAPI,

    FeatureAccessEndpoints,
    Meta_Endpoints,
    Meta_Endpoints_v2,
    FeatureDataEndpoints,
    SingleFeatureDataAccess,
    Pairwise_Endpoints,
    SeqPeekViewDataAccessAPI
    # User_Endpoints
])

