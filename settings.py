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

import os
from os.path import join, dirname, exists
import sys
from pathlib import Path
from dotenv import load_dotenv
from socket import gethostname, gethostbyname


SECURE_LOCAL_PATH = os.environ.get('SECURE_LOCAL_PATH', '')

if not exists(join(dirname(__file__), SECURE_LOCAL_PATH, '.env')):
    print("[ERROR] Couldn't open .env file expected at {}!".format(
        join(dirname(__file__), SECURE_LOCAL_PATH, '.env'))
    )
    print("[ERROR] Exiting settings.py load - check your Pycharm settings and secure_path.env file.")
    exit(1)

load_dotenv(dotenv_path=join(dirname(__file__), SECURE_LOCAL_PATH, '.env'))

APP_ENGINE_FLEX = 'aef-'
APP_ENGINE = 'Google App Engine/'
API_VERSION = 'v1'


BASE_DIR                = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + os.sep

DEBUG                   = (os.environ.get('DEBUG', 'False') == 'True')

DEBUG_API_ID            = os.getenv('DEBUG_API_ID','')
DEBUG_API_EMAIL            = os.getenv('DEBUG_API_EMAIL','')

print("[STATUS] DEBUG mode is "+str(DEBUG))

LOGGER_NAME = os.environ.get('API_LOGGER_NAME', 'main_logger')

BASE_URL                = os.environ.get('BASE_URL', 'https://idc-dev.appspot.com')
BASE_API_URL            = os.environ.get('BASE_API_URL', 'https://api-dot-idc-dev.appspot.com')

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

PAGE_TOKEN_KEY          = os.environ.get('PAGE_TOKEN_KEY', '')

GOOGLE_APPLICATION_CREDENTIALS  = join(dirname(__file__), SECURE_LOCAL_PATH, os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''))
OAUTH2_CLIENT_ID                = os.environ.get('OAUTH2_CLIENT_ID', '')
OAUTH2_CLIENT_SECRET            = os.environ.get('OAUTH2_CLIENT_SECRET', '')

API_CLIENT_ID  = os.environ.get('API_CLIENT_ID', '')
API_AUTH_TOKEN = ''
try:
    with open(join(dirname(__file__), SECURE_LOCAL_PATH, os.environ.get('API_TOKEN_FILE', '')), 'r') as filehandle:
        API_AUTH_TOKEN = filehandle.read()
except Exception:
    print("[ERROR] Failed to load API auth token - authorized endpoints may fail!")
API_VERSION = 'v1'

##############################################################
#   MAXes to prevent size-limited events from causing errors
# These are really here to satisfy some definitions in the bq_helpers.py
# dependency chain.

# Google App Engine has a response size limit of 32M. ~65k entries from the cohort_filelist view will
# equal just under the 32M limit. If each individual listing is ever lengthened or shortened this
# number should be adjusted
MAX_FILE_LIST_REQUEST = 65000
MAX_BQ_RECORD_RESULT = int(os.environ.get('MAX_BQ_RECORD_RESULT', '5000'))

# IGV limit to prevent users from trying ot open dozens of files
MAX_FILES_IGV = 5

# Rough max file size to allow for eg. barcode list upload, to revent triggering RequestDataTooBig
FILE_SIZE_UPLOAD_MAX = 1950000
##############################################################

# IGV limit to prevent users from trying to open dozens of files
MAX_FILES_IGV = 5

BQ_MAX_ATTEMPTS             = int(os.environ.get('BQ_MAX_ATTEMPTS', '30'))
MAX_BQ_INSERT                        = int(os.environ.get('MAX_BQ_INSERT', '500'))

GCLOUD_PROJECT_ID              = os.environ.get('GCLOUD_PROJECT_ID', '')
GCLOUD_PROJECT_NUMBER          = os.environ.get('GCLOUD_PROJECT_NUMBER', '')
BIGQUERY_PROJECT_ID            = os.environ.get('BIGQUERY_PROJECT_ID', GCLOUD_PROJECT_ID)
BIGQUERY_DATA_PROJECT_ID       = os.environ.get('BIGQUERY_DATA_PROJECT_ID', GCLOUD_PROJECT_ID)


# Explicitly check for known items
BLACKLIST_RE = r'((?i)<script>|(?i)</script>|!\[\]|!!\[\]|\[\]\[\".*\"\]|(?i)<iframe>|(?i)</iframe>)'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = os.environ.get('STATIC_URL', '/static/')

IS_DEV = (os.environ.get('IS_DEV', 'False') == 'True')