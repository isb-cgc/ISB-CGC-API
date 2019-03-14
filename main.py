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
from google.cloud import logging
import os

from flask import Flask, jsonify, request
from flask_cors import cross_origin
import cohorts.views

client = logging.Client()
handler = client.get_default_handler()
cloud_logger = logging.getLogger(__name__)
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(handler)

app = Flask(__name__)


@app.route('/apiv4', methods=['GET', 'POST'])
def base():
    """Base response"""
    logger.error("[ERROR] Directory listing: ")
    logger.error(os.listdir('./'))
    logger.info("[INFO] Directory listing: ")
    logger.info(os.listdir('./'))
    response = jsonify({
        'code': 200,
        'message': 'Welcome to the ISB-CGC API, Version 4.'
    })
    response.status_code = 200
    return response


# Error handlers
@app.errorhandler(500)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    logging.exception('An error occured while processing the request.')
    response = jsonify({
        'code': 500,
        'message': 'Exception: {}'.format(e)})
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
