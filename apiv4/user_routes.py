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
import json
from flask import jsonify, request, redirect, url_for
from apiv4 import app
from auth import auth_info, UserValidationException, validate_user, get_user
from user_views import get_account_details
from django.conf import settings
from django.db import close_old_connections
from api_logging import *

HTTP_301_MOVED_PERMANENTLY = 301

logger = logging.getLogger(settings.LOGGER_NAME)


@app.route('/v4/users/account_details/', methods=['GET'], strict_slashes=False)
def account_details():
    response = jsonify({
        'code': 405,
        'message': "The 'account details' path has been deprecated in version 4.2 due to the removal of controlled access data registration at ISB-CGC."
    })

    response.status_code = 405

    return response
