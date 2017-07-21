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
from protorpc import remote, messages

from dataset_utils.dataset_access_support_factory import DatasetAccessSupportFactory

logger = logging.getLogger(__name__)

class UserGetAPIReturnJSON(messages.Message):
    message = messages.StringField(1)
    dbGaP_authorized = messages.BooleanField(2)
    dbGaP_allowed = messages.BooleanField(3)

class UserGetAPICommon(remote.Service):
    def get(self, program):
        '''
        Returns the dbGaP authorization status of the user.
        '''
        user_email = None

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        if user_email is None:
            raise endpoints.UnauthorizedException("Authentication unsuccessful.")

        das = DatasetAccessSupportFactory.from_webapp_django_settings()
        authorized_datasets = das.get_datasets_for_era_login(user_email)
        all_datasets = das.get_all_datasets_and_google_groups()
        
        authorized = False
        allowed = False
        for dataset in authorized_datasets:
            if program in dataset:
                authorized = True
                allowed = True
        if not allowed:
            for dataset in all_datasets:
                if program in dataset:
                    allowed = True
            
        if not allowed:
            return UserGetAPIReturnJSON(message="{} is not on the controlled-access google group.".format(user_email),
                              dbGaP_authorized=False)
        # since user has access to the program controlled data, include a warning
        warn_message = 'You are reminded that when accessing controlled access information you are bound by the dbGaP DATA USE CERTIFICATION AGREEMENT (DUCA) for this dataset.'
        if authorized:
            return UserGetAPIReturnJSON(message="{} has dbGaP authorization for {} and is a member of the controlled-access google group.  {}"
                              .format(user_email, program, warn_message),
                              dbGaP_authorized=True,
                              dbGaP_allowed=True)
        else:
            return UserGetAPIReturnJSON(message="{} has dbGaP authorization for {} but is not currently a member of the controlled-access google group.  {}"
                              .format(user_email, program, warn_message),
                              dbGaP_authorized=False,
                              dbGaP_allowed=True)
