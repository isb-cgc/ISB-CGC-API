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

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from accounts.models import AuthorizedDataset, NIH_User, UserAuthorizedDatasets
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

        authorized = False
        allowed = False
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist, MultipleObjectsReturned:
            user = None

        if user:
            # FIND NIH_USER FOR USER
            try:
                nih_user = NIH_User.objects.filter(user=user).first()
            except:
                nih_user = None
    
            # IF USER HAS LINKED ERA COMMONS ID
            if nih_user:
                # FIND ALL DATASETS USER HAS ACCESS TO
                user_auth_datasets = AuthorizedDataset.objects.filter(id__in=UserAuthorizedDatasets.objects.filter(nih_user_id=nih_user.id).values_list('authorized_dataset', flat=True))
                for dataset in user_auth_datasets:
                    if program in dataset.name:
                        authorized = True
                        allowed = True

        if not allowed:
            return UserGetAPIReturnJSON(message="{} is not on the controlled-access google group.".format(user_email),
                              dbGaP_authorized=False,
                              dbGaP_allowed=False)
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
