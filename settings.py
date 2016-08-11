"""

Copyright 2016, Institute for Systems Biology

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
import django

# Django settings for GAE_Django17 project.
import os

import django

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DEBUG')
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST')
]

### added for connecting to CloudSQL with SSL certs on MVM platform
SSL_DIR = os.path.abspath(os.path.dirname(__file__))+os.sep

#ADMINS = (
    # ('Your Name', 'your_email@example.com'),
#)
ADMINS = ()
MANAGERS = ADMINS

REQUEST_PROJECT_EMAIL = os.environ.get('REQUEST_PROJECT_EMAIL')

PROJECT_ID = os.environ.get('PROJECT_ID')
BQ_PROJECT_ID = os.environ.get('BQ_PROJECT_ID')
IGV_PROJECT_ID = os.environ.get('IGV_PROJECT_ID')

CLOUD_BASE_URL = os.environ.get('CLOUD_BASE_URL')
CLOUD_API_URL = os.environ.get('CLOUD_API_URL')
LOCAL_BASE_URL = os.environ.get('LOCAL_BASE_URL')

# Compute services
PAIRWISE_SERVICE_URL = os.environ.get('PAIRWISE_SERVICE_URL')

# Data Buckets
OPEN_DATA_BUCKET = os.environ.get('OPEN_DATA_BUCKET')
DCC_CONTROLLED_DATA_BUCKET = os.environ.get('DCC_CONTROLLED_DATA_BUCKET')
CGHUB_CONTROLLED_DATA_BUCKET = os.environ.get('CGHUB_CONTROLLED_DATA_BUCKET')

GCLOUD_BUCKET = os.environ.get('GCLOUD_BUCKET')

# BigQuery cohort storage settings
COHORT_DATASET_ID = os.environ.get('COHORT_DATASET_ID')
DEVELOPER_COHORT_TABLE_ID = os.environ.get('DEVELOPER_COHORT_TABLE_ID')

NIH_AUTH_ON = os.environ.get('NIH_AUTH_ON', False)

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.mysql'),
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
        # 'PORT': os.environ.get('DATABASE_PORT', 3306),
        'NAME': os.environ.get('DATABASE_NAME', 'dev'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD')
    }
}

if os.environ.has_key('DB_SSL_CERT'):
    DATABASES['default']['OPTIONS'] = {
        'ssl': {
            'ca': os.environ.get('DB_SSL_CA'),
            'cert': os.environ.get('DB_SSL_CERT'),
            'key': os.environ.get('DB_SSL_KEY')
        }
    }
BASE_URL = CLOUD_BASE_URL
BASE_API_URL = CLOUD_API_URL
SITE_ID = 4


# For running local unit tests for models
import sys
if 'test' in sys.argv:
    DATABASES = os.environ.get('TEST_DATABASE')

def get_project_identifier():
    return BQ_PROJECT_ID

BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET')
BIGQUERY_DATASET2 = os.environ.get('BIGQUERY_DATASET2')

def get_bigquery_dataset():
    return BIGQUERY_DATASET

PROJECT_NAME = os.environ.get('PROJECT_NAME')
BIGQUERY_PROJECT_NAME = os.environ.get('BIGQUERY_PROJECT_NAME')

def get_bigquery_project_name():
    return BIGQUERY_PROJECT_NAME

# Set cohort table here
if DEVELOPER_COHORT_TABLE_ID is None:
    raise Exception("Developer-specific cohort table ID is not set.")

class BigQueryCohortStorageSettings(object):
    def __init__(self, dataset_id, table_id):
        self.dataset_id = dataset_id
        self.table_id = table_id

def GET_BQ_COHORT_SETTINGS():
    return BigQueryCohortStorageSettings(COHORT_DATASET_ID, DEVELOPER_COHORT_TABLE_ID)

USE_CLOUD_STORAGE = os.environ.get('USE_CLOUD_STORAGE')

PROCESSING_ENABLED = os.environ.get('PROCESSING_ENABLED')
PROCESSING_JENKINS_URL = os.environ.get('PROCESSING_JENKINS_URL')
PROCESSING_JENKINS_PROJECT = os.environ.get('PROCESSING_JENKINS_PROJECT')
PROCESSING_JENKINS_USER = os.environ.get('PROCESSING_JENKINS_USER')
PROCESSING_JENKINS_PASSWORD = os.environ.get('PROCESSING_JENKINS_PASSWORD')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_FOLDER = os.environ.get('MEDIA_FOLDER')
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', os.environ.get('MEDIA_FOLDER'))
MEDIA_ROOT = os.path.normpath(MEDIA_ROOT)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
# SECRET_KEY = os.environ.get('SECRET_KEY')

MIDDLEWARE_CLASSES = (
    # For using NDB with Django
    # documentation: https://cloud.google.com/appengine/docs/python/ndb/#integration
    'google.appengine.ext.ndb.django_middleware.NdbDjangoMiddleware',
    'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

ROOT_URLCONF = 'GenespotRE.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'GenespotRE.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.admin',
    # 'django.contrib.admindocs',
    # 'GenespotRE',
    # 'visualizations',
    # 'seqpeek',
    'sharing',
    'cohorts',
    'projects',
    # 'genes',
    # 'variables',
    # 'workbooks',
    'data_upload'
)

#############################
#  django-session-security  #
#############################

# testing "session security works at the moment" commit
# INSTALLED_APPS += ('session_security',)
# SESSION_SECURITY_WARN_AFTER = 540
# SESSION_SECURITY_EXPIRE_AFTER = 600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
MIDDLEWARE_CLASSES += (
    # for django-session-security -- must go *after* AuthenticationMiddleware
    # 'session_security.middleware.SessionSecurityMiddleware',
)

###############################
# End django-session-security #
###############################

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

##########################
#  Start django-allauth  #
##########################

LOGIN_REDIRECT_URL = '/dashboard/'

INSTALLED_APPS += (
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google')

# Template Engine Settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # add any necessary template paths here
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'accounts'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            # add any context processors here
            'context_processors': (
                'allauth.socialaccount.context_processors.socialaccount',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.tz',
                'finalware.context_processors.contextify',
                'GenespotRE.context_processor.additional_context',
            ),
            # add any loaders here; if using the defaults, we can comment it out
            # 'loaders': (
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader'
            # ),
            'debug': DEBUG,
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOCIALACCOUNT_PROVIDERS = \
    { 'google':
        { 'SCOPE': ['profile', 'email'],
          'AUTH_PARAMS': { 'access_type': 'online' }
        }
    }


##########################
#   End django-allauth   #
##########################

GOOGLE_APPLICATION_CREDENTIALS  = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
CLIENT_SECRETS                  = os.environ.get('CLIENT_SECRETS')
PEM_FILE                        = os.environ.get('PEM_FILE')
CLIENT_EMAIL                    = os.environ.get('CLIENT_EMAIL')
WEB_CLIENT_ID                   = os.environ.get('WEB_CLIENT_ID')
INSTALLED_APP_CLIENT_ID         = os.environ.get('INSTALLED_APP_CLIENT_ID')

#################################
#   For NIH/eRA Commons login   #
#################################

LOGIN_EXPIRATION_HOURS = 24
FAKE_DBGAP_AUTHENTICATION_LIST_FILENAME  = os.environ.get('FAKE_DBGAP_AUTHENTICATION_LIST_FILENAME')
DBGAP_AUTHENTICATION_LIST_FILENAME  = os.environ.get('DBGAP_AUTHENTICATION_LIST_FILENAME')
DBGAP_AUTHENTICATION_LIST_BUCKET    = os.environ.get('DBGAP_AUTHENTICATION_LIST_BUCKET')
ACL_GOOGLE_GROUP                    = os.environ.get('ACL_GOOGLE_GROUP')
OPEN_ACL_GOOGLE_GROUP               = os.environ.get('OPEN_ACL_GOOGLE_GROUP')
ERA_LOGIN_URL                       = os.environ.get('ERA_LOGIN_URL')
IPV4                                = os.environ.get('IPV4')
SAML_FOLDER                         = os.environ.get('SAML_FOLDER')

######################################
#   For directory, reports services  #
######################################
GOOGLE_GROUP_WEBAPP_ADMIN           = os.environ.get('GOOGLE_GROUP_WEBAPP_ADMIN', '')
GOOGLE_GROUP_API_ADMIN           = os.environ.get('GOOGLE_GROUP_API_ADMIN', '')

##############################
#   Start django-finalware   #
##############################

INSTALLED_APPS += (
    'finalware',)

SITE_SUPERUSER_USERNAME = os.environ.get('SU_USER')
SITE_SUPERUSER_EMAIL = ''
SITE_SUPERUSER_PASSWORD = os.environ.get('SU_PASS')

############################
#   End django-finalware   #
############################

CONN_MAX_AGE = 0

# Initialize Django (when running ISB-CGC-API as standalone using dev_appserver.py)
django.setup()
