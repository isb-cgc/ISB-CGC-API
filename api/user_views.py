# 
# Copyright 2019, Institute for Systems Biology
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging

from python_settings import settings
from . auth import UserValidationException

logger = logging.getLogger(settings.LOGGER_NAME)


def get_account_details(user):
    accounts_details = None

    try:
        accounts_details = {}

    except UserValidationException as u:
        logger.warning(u)
        accounts_details = {'message': str(u)}

    except Exception as e:
        logger.error("[ERROR] Encountered an error while retrieving user account details:")
        logger.exception(e)
        accounts_details = {'message': "Encountered an error while retrieving account details for {}.".format(user.email)}

    return accounts_details
