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
import logging

import endpoints
from protorpc import messages

from api_3.isb_cgc_api_TCGA.annotations_api import AnnotationAPI, MetadataAnnotationList
from api_3.isb_cgc_api_TCGA.isb_cgc_api_helpers import ISB_CGC_TCGA_Endpoints

logger = logging.getLogger(__name__)


class CasesAnnotationsQueryBuilder(object):

    @staticmethod
    def build_query(entity_types=None):
        query_str = 'select * ' \
                    'from TCGA_metadata_annotation ' \
                    'where case_barcode=%s and status = "Approved" '
        if len(entity_types) > 0:
            query_str += 'and entity_type in (' + ', '.join(['%s']*len(entity_types)) + ')'
        
        return query_str

    @staticmethod
    def build_metadata_query():
        query_str = 'select case_barcode ' \
                    'from TCGA_metadata_clinical ' \
                    'where case_barcode=%s '

        return query_str

@ISB_CGC_TCGA_Endpoints.api_class(resource_name='cases')
class TCGA_CasesAnnotationAPI(AnnotationAPI):

    GET_RESOURCE = endpoints.ResourceContainer(case_barcode=messages.StringField(1, required=True),
                                               entity_type=messages.StringField(2, repeated=True))

    @endpoints.method(GET_RESOURCE, MetadataAnnotationList,
                      path='cases/{case_barcode}/annotations', http_method='GET')
    def annotations(self, request):
        """
        Returns TCGA annotations about a specific sample,
        Takes a case barcode (of length 12, *eg* TCGA-01-0628) as a required parameter.
        User does not need to be authenticated.
        """
        return self.process_annotations(request, 'case_barcode', CasesAnnotationsQueryBuilder(), logger)


    def validate_barcode(self, case_barcode):
        # check to make sure case_barcode is in correct form
        parts = case_barcode.split('-')
        assert len(parts) == 3
        assert len(parts[0]) == 4
        assert len(parts[1]) == 2
        assert len(parts[2]) == 4
