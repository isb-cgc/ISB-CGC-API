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
from protorpc import message_types

from api_3.users_get_common import UserGetAPICommon, UserGetAPIReturnJSON
from api_3.isb_cgc_api_TCGA.isb_cgc_api_helpers import ISB_CGC_TCGA_Endpoints

@ISB_CGC_TCGA_Endpoints.api_class(resource_name='users')
class TCGA_UserGetAPI(UserGetAPICommon):

    @endpoints.method(message_types.VoidMessage, UserGetAPIReturnJSON, http_method='GET', path='users')
    def get(self, request):
        '''
        Returns the dbGaP authorization status of the user.
        '''
        return super(TCGA_UserGetAPI, self).get(request)
