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

class AliquotsAnnotationsQueryBuilder(object):

    @staticmethod
    def build_query(entity_types=None):
        query_str = 'select * ' \
                    'from TCGA_metadata_annotation ' \
                    'where aliquot_barcode=%s and status = "Approved" '
        if len(entity_types) > 0:
            query_str += 'and entity_type in (' + ', '.join(['%s']*len(entity_types)) + ')'
        
        return query_str

    @staticmethod
    def build_metadata_query():
        return 'select * from TCGA_metadata_data_HG19 where aliquot_barcode=%s ' \
            'union ' \
            'select * from TCGA_metadata_data_HG38 where aliquot_barcode=%s'

@ISB_CGC_TCGA_Endpoints.api_class(resource_name='aliquots')
class TCGA_AliquotsAnnotationAPI(AnnotationAPI):

    GET_RESOURCE = endpoints.ResourceContainer(aliquot_barcode=messages.StringField(1, required=True),
                                               entity_type=messages.StringField(2, repeated=True))

    @endpoints.method(GET_RESOURCE, MetadataAnnotationList,
                      path='aliquots/{aliquot_barcode}/annotations', http_method='GET')
    def annotations(self, request):
        """
        Returns TCGA annotations about a specific aliquot,
        Takes an aliquot barcode (of length , *eg* TCGA-01-0628-11A-01D-0356-01) as a required parameter.
        User does not need to be authenticated.
        """
        return self.process_annotations(request, 'aliquot_barcode', AliquotsAnnotationsQueryBuilder(), logger)


    def validate_barcode(self, aliquot_barcode):
        # check to make sure aliquot_barcode is in correct form
            parts = aliquot_barcode.split('-')
            assert len(parts) == 7
            assert len(parts[0]) == 4
            assert len(parts[1]) == 2
            assert len(parts[2]) == 4
            assert len(parts[3]) == 3
            assert len(parts[4]) in [2, 3]
            assert len(parts[5]) == 4
            assert len(parts[6]) == 2

