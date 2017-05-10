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

from api_3.isb_cgc_api.isb_cgc_api_helpers import ISB_CGC_Endpoints
from api_3.cloudstoragefilepaths_helper import GCSFilePathList, CohortsCloudStorageFilePathsHelper

@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortsCloudStorageFilePathsAPI(CohortsCloudStorageFilePathsHelper):

    def build_program_query(self, final_query_str, query_tuple, program, param_map, build):
        query_str = 'SELECT md.file_name_key, md.access '\
        'FROM {}_metadata_data_{} md '.format(program, build)
        query_str += 'JOIN cohorts_samples cs ON md.sample_barcode=cs.sample_barcode WHERE cs.cohort_id=%s '
        query_tuple += [param_map['cohort_id']]
        query_str += 'AND file_name_key != "" AND file_name_key is not null '
        for field, value in param_map.iteritems():
            if field not in ['limit', 'cohort_id', 'sample_barcode', 'genomic_build'] and value:
                query_str += ' and md.{}=%s '.format(field)
                query_tuple += [value]
        
        query_str += ' GROUP BY md.file_name_key, md.access '
        if 0 < len(final_query_str):
            final_query_str += ' UNION '
        final_query_str += query_str
        return final_query_str, query_tuple

    def build_query(self, param_map, program):
        builds = self.get_genomic_builds(param_map, '')
        final_query_str = ''
        query_tuple = []
        for program in ('CCLE', 'TARGET', 'TCGA'):
            for build in builds:
                final_query_str, query_tuple = self.build_program_query(final_query_str, query_tuple, program, param_map, build)
        
        if 'limit' in param_map and param_map['limit']:
            final_query_str += ' LIMIT %s'  
            query_tuple += [param_map['limit']]
        else:
            final_query_str += ' LIMIT 10000'
        return final_query_str, query_tuple

    @endpoints.method(CohortsCloudStorageFilePathsHelper.GET_RESOURCE, GCSFilePathList,  http_method='GET',
                      path='cohorts/{cohort_id}/cloud_storage_file_paths')
    def cloud_storage_file_paths(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        return super(CohortsCloudStorageFilePathsAPI, self).cloud_storage_file_paths(request)
