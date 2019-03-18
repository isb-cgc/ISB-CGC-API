"""

Copyright 2019, Institute for Systems Biology

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
import json
from flask import jsonify, request

from apiv4 import app


@app.route('/apiv4', methods=['GET', 'POST'])
def apiv4():
    """Base response"""
    response = jsonify({
        'code': 200,
        'message': 'Welcome to the ISB-CGC API, Version 4.'
    })
    response.status_code = 200
    return response


@app.route('/apiv4/programs', methods=['GET'])
def programs():
    """List the programs currently available on this API"""
    response = jsonify({
        'code': 200,
        'message': 'TCGA (HG19, HG38); TARGET (HG19, HG38), CCLE (HG19)'
    })
    response.status_code = 200
    return response
