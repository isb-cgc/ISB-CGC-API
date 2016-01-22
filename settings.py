import os

### MVM STUFF
SSL_DIR = os.path.abspath(os.path.dirname(__file__))+os.sep
if 'VERSION_NAME' in os.environ:
    VER = os.getenv('VERSION_NAME')
else:
    VER = os.getenv('SETTINGS_VERSION')
###


# if os.getenv('SETTINGS_VERSION') == 'dev':
SETTINGS = {
    'SECRET_KEY': '$czh)t*on8g-l+q4io=*7x4$z!0w+lfz71ya1+$9^6rkphzi18',
    'DEBUG': True,
    'PROJECT_ID': '907668440978',
    'BQ_PROJECT_ID': '907668440978',

    'CLOUD_BASE_URL': 'http://api.isb-cgc.appspot.com',
    'CLOUD_API_URL': 'https://api.isb-cgc.appspot.com',

    'LOCAL_BASE_URL': 'http://localhost:8080',


    # BigQuery cohort storage settings
    'COHORT_DATASET_ID': 'dev_deployment_cohorts',
    'DEVELOPER_COHORT_TABLE_ID': 'pl_cohorts',
    'CLOUD_COHORT_TABLE': 'dev_cohorts',

    # Database settings
    'CLOUD_DATABASE': {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dev',
            'USER': 'root',
            'PASSWORD': 'password', # this is particular to isb-cgc:mvm CldSQL Instance
            'HOST':   '/cloudsql/isb-cgc:demo01',
            # 'PORT': 3306,
            'OPTIONS':  {
                'ssl': {'ca': SSL_DIR + 'demo01-server-ca.pem',
                        'cert': SSL_DIR + 'demo01-client-cert.pem',
                        'key': SSL_DIR + 'demo01-client-key.pem'
                        }
            }
        }
    },
    'CLOUD_DATABASE_LOCAL_CONNECTION': {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '173.194.225.46',
            'NAME': 'dev',
            'USER': 'root',
            'PASSWORD': 'password'
        }
    },
    'LOCAL_DATABASE': {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dev',
            'USER': 'root',
            'PASSWORD': 'password'
        }
    },
    'TEST_DATABASE': {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'djangotests',
            'USER': 'root',
            'PASSWORD': 'password'
        }
    },
    'BIGQUERY_DATASET': 'isb_cgc',
    'BIGQUERY_DATASET2': 'tcga_data_open',
    'BIGQUERY_PROJECT_NAME': 'isb-cgc',

    'GOOGLE_APPLICATION_CREDENTIALS': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'privatekey.json'),
    'CLIENT_SECRETS': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secrets.json'),
    'PEM_FILE': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'privatekey.pem'),
    'CLIENT_EMAIL': '907668440978-oskt05du3ao083cke14641u35deokgjj@developer.gserviceaccount.com',
    'WEB_CLIENT_ID': '907668440978-j9ec27vhg0e0mmpjvrcelfq7ah9n0ntm.apps.googleusercontent.com',
    'INSTALLED_APP_CLIENT_ID': '907668440978-0ol0griu70qkeb6k3gnn2vipfa5mgl60.apps.googleusercontent.com',

    'DBGAP_AUTHENTICATION_LIST_FILENAME': 'dbGaP_authentication_list',
    'DBGAP_AUTHENTICATION_LIST_BUCKET': 'isb-cgc-nih-users',
    'ACL_GOOGLE_GROUP': 'isb-cgc-cntl@isb-cgc.org',
    'OPEN_ACL_GOOGLE_GROUP': 'isb-cgc-open@isb-cgc.org',
    'ERA_LOGIN_URL': 'https://104.197.85.205/',
    'IPV4': '173.194.225.46',

    # Compute services
    'PAIRWISE_SERVICE_URL': 'http://104.197.42.216:8080',

    # Cloud Storage Buckets
    'OPEN_DATA_BUCKET': 'isb-cgc-open',
    'CONTROLLED_DATA_BUCKET': 'isb-cgc-controlled'
}

# elif os.getenv('SETTINGS_VERSION') == 'test':
#     SETTINGS = {
#         'SECRET_KEY': '$czh)t*on8g-l+q4io=*7x4$z!0w+lfz71ya1+$9^6rkphzi18',
#         'DEBUG': True,
#         'PROJECT_ID': '144657163696',
#         'BQ_PROJECT_ID': '144657163696',
#
#         'CLOUD_BASE_URL': 'http://isb-cgc-test.appspot.com',
#         'CLOUD_API_URL': 'https://isb-cgc-test.appspot.com',
#
#         'LOCAL_BASE_URL': 'http://localhost:8080',
#
#
#         # BigQuery cohort storage settings
#         'COHORT_DATASET_ID': 'cloud_deployment_cohorts',
#         'DEVELOPER_COHORT_TABLE_ID': 'prod_cohorts',
#         'CLOUD_COHORT_TABLE': 'prod_cohorts',
#
#         # Database Settings
#         'CLOUD_DATABASE': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': 'test',
#                 'USER': 'django-user',
#                 'PASSWORD': 'isbcgc2015', # this is particular to isb-cgc:mvm CldSQL Instance
#                 'HOST':   '173.194.255.207',
#                 'PORT': 3306,
#                 'OPTIONS':  {
#                     'ssl': {
#                         'ca': SSL_DIR + 'ISB-CGC-test-main-server-ca.pem',
#                         'cert': SSL_DIR + 'ISB-CGC-test-main-client-cert.pem',
#                         'key': SSL_DIR + 'ISB-CGC-test-main-client-key.pem'
#                     }
#                 }
#             }
#         },
#         'CLOUD_DATABASE_LOCAL_CONNECTION': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'HOST': '173.194.255.207',
#                 'NAME': 'test',
#                 'USER': 'plee',
#                 'PASSWORD': 'password'
#             }
#         },
#         'LOCAL_DATABASE': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': 'dev',
#                 'USER': 'root',
#                 'PASSWORD': 'password'
#             }
#         },
#
#         # 'BIGQUERY_DATASET': 'isb_cgc',
#         'BIGQUERY_DATASET': 'tcga_data_open',
#         'BIGQUERY_DATASET2': 'tcga_data_open',
#         'BIGQUERY_PROJECT_NAME': 'isb-cgc-test',
#
#         'GOOGLE_APPLICATION_CREDENTIALS_ISB_CGC': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'privatekey.json'),
#         'GOOGLE_APPLICATION_CREDENTIALS': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ISB-CGC-test-privatekey.json'), # for service account
#         'CLIENT_SECRETS': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ISB-CGC-test-client-secrets.json'),  # for web client
#         'PEM_FILE': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ISB-CGC-test-privatekey.pem'),  # 'ISB-CGC-test-4b595aaa1759.p12'),
#         'CLIENT_EMAIL': '144657163696-utjumdn9c03fof16ig7bjak44hfj53o6@developer.gserviceaccount.com',
#         'WEB_CLIENT_ID': '144657163696-glkmo9pq3hts8l0002utth0013rrm0vf.apps.googleusercontent.com',
#         'INSTALLED_APP_CLIENT_ID': '144657163696-9dnmed5krg4r00km2fg1q93l71nj3r9j.apps.googleusercontent.com',
#
#         'DBGAP_AUTHENTICATION_LIST_FILENAME': 'dbGaP_authentication_list',
#         'DBGAP_AUTHENTICATION_LIST_BUCKET': 'isb-cgc-nih-users',
#         'ACL_GOOGLE_GROUP': 'isb-cgc-cntl@isb-cgc.org',
#         'OPEN_ACL_GOOGLE_GROUP': 'isb-cgc-open@isb-cgc.org',
#         'ERA_LOGIN_URL': 'https://104.197.85.205/',
#         'IPV4': '173.194.225.46',
#
#         # Compute services
# 		'PAIRWISE_SERVICE_URL': 'http://104.197.42.216:8080',
#
#         # Cloud Storage Buckets
#         'OPEN_DATA_BUCKET': 'isb-cgc-open',
#         'CONTROLLED_DATA_BUCKET': 'isb-cgc-controlled'
#     }
#
# elif os.getenv('SETTINGS_VERSION') == 'stage':
#     SETTINGS = {
#         'SECRET_KEY': '$czh)t*on8g-l+q4io=*7x4$z!0w+lfz71ya1+$9^6rkphzi18',
#         'DEBUG': True,
#         'PROJECT_ID': '241915578225',
#         'BQ_PROJECT_ID': '241915578225',
#
#         'CLOUD_BASE_URL': 'http://isb-cgc-stage.appspot.com',
#         'CLOUD_API_URL': 'https://isb-cgc-stage.appspot.com',
#
#         'LOCAL_BASE_URL': 'http://localhost:8080',
#
#
#         # BigQuery cohort storage settings
#         'COHORT_DATASET_ID': 'cloud_deployment_cohorts',
#         'DEVELOPER_COHORT_TABLE_ID': 'prod_cohorts',
#         'CLOUD_COHORT_TABLE': 'prod_cohorts',
#
#         # Database Settings
#         'CLOUD_DATABASE': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': 'main',
#                 'USER': 'root',
#                 'PASSWORD': 'isbcgctest', # this is particular to isb-cgc:mvm CldSQL Instance
#                 'HOST':   '173.194.235.45',
#                 'PORT': 3306,
#                 'OPTIONS':  {
#                     'ssl': {'ca': SSL_DIR + 'ISB-CGC-stage-server-ca.pem',
#                             'cert': SSL_DIR + 'ISB-CGC-stage-client-cert.pem',
#                             'key': SSL_DIR + 'ISB-CGC-stage-client-key.pem'
#                             }
#                 }
#             }
#         },
#         'CLOUD_DATABASE_LOCAL_CONNECTION': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'HOST': '173.194.235.45',
#                 'NAME': 'main',
#                 'USER': 'root',
#                 'PASSWORD': 'isbcgctest'
#             }
#         },
#         'LOCAL_DATABASE': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': 'dev',
#                 'USER': 'root',
#                 'PASSWORD': 'password'
#             }
#         },
#
#         # 'BIGQUERY_DATASET': 'isb_cgc',
#         'BIGQUERY_DATASET': 'tcga_data_open',
#         'BIGQUERY_DATASET2': 'tcga_data_open',
#         'BIGQUERY_PROJECT_NAME': 'isb-cgc-stage',
#
#         'GOOGLE_APPLICATION_CREDENTIALS_ISB_CGC': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'privatekey.json'),
#         'GOOGLE_APPLICATION_CREDENTIALS': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ISB-CGC-stage-privatekey2.json'), # for service account
#         'CLIENT_SECRETS': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ISB-CGC-stage-client-secrets.json'),  # for web client
#         'PEM_FILE': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ISB-CGC-stage-privatekey2.pem'),  # 'ISB-CGC-stage-privatekey.p12'),
#         'CLIENT_EMAIL': '241915578225-nuanneqc1tdeqi0fthog1g0fl8n29a1k@developer.gserviceaccount.com',
#         'WEB_CLIENT_ID': '241915578225-jh43cpemj9tgfh432d8qmidl70epss45.apps.googleusercontent.com',
#         'INSTALLED_APP_CLIENT_ID': '241915578225-nuanneqc1tdeqi0fthog1g0fl8n29a1k.apps.googleusercontent.com',
#
#         'DBGAP_AUTHENTICATION_LIST_FILENAME': 'dbGaP_authentication_list',
#         'DBGAP_AUTHENTICATION_LIST_BUCKET': 'isb-cgc-nih-users',
#         'ACL_GOOGLE_GROUP': 'isb-cgc-cntl@isb-cgc.org',
#         'OPEN_ACL_GOOGLE_GROUP': 'isb-cgc-open@isb-cgc.org',
#         'ERA_LOGIN_URL': 'https://104.197.85.205/',
#         'IPV4': '173.194.225.46',
#
#         # Compute services
# 		'PAIRWISE_SERVICE_URL': 'http://104.197.42.216:8080',
#
#         # Cloud Storage Buckets
#         'OPEN_DATA_BUCKET': 'isb-cgc-open',
#         'CONTROLLED_DATA_BUCKET': 'isb-cgc-controlled'
#     }
#
# elif os.getenv('SETTINGS_VERSION') == 'prod':
#     SETTINGS = {
#         'SECRET_KEY': '$czh)t*on8g-l+q4io=*7x4$z!0w+lfz71ya1+$9^6rkphzi18',
#         'DEBUG': True,
#         'PROJECT_ID': '907668440978',
#         'BQ_PROJECT_ID': '907668440978',
#
#         'CLOUD_BASE_URL': 'http://isb-cgc.appspot.com',
#         'CLOUD_API_URL': 'https://isb-cgc.appspot.com',
#
#         'LOCAL_BASE_URL': 'http://localhost:8080',
#
#
#         # BigQuery cohort storage settings
#         'COHORT_DATASET_ID': 'cloud_deployment_cohorts',
#         'DEVELOPER_COHORT_TABLE_ID': 'pl_cohorts',
#         'CLOUD_COHORT_TABLE': 'prod_cohorts',
#
#         # Database settings
#         'CLOUD_DATABASE': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'HOST': '/cloudsql/isb-cgc:demo01',
#                 'NAME': 'dev',
#                 'USER': 'django-app'
#             }
#         },
#         'CLOUD_DATABASE_LOCAL_CONNECTION': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'HOST': '173.194.225.46',
#                 'NAME': 'dev',
#                 'USER': 'root',
#                 'PASSWORD': 'password'
#             }
#         },
#         'LOCAL_DATABASE': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': 'dev',
#                 'USER': 'root',
#                 'PASSWORD': 'password'
#             }
#         },
#         'TEST_DATABASE': {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': 'djangotests',
#                 'USER': 'root',
#                 'PASSWORD': 'password'
#             }
#         },
#
#         'BIGQUERY_DATASET': 'isb_cgc',
#         'BIGQUERY_DATASET2': 'tcga_data_open',
#         'BIGQUERY_PROJECT_NAME': 'isb-cgc',
#
#         'GOOGLE_APPLICATION_CREDENTIALS': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'privatekey.json'),
#         'CLIENT_SECRETS': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secrets.json'),
#         'PEM_FILE': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'privatekey.pem'),
#         'CLIENT_EMAIL': '907668440978-oskt05du3ao083cke14641u35deokgjj@developer.gserviceaccount.com',
#         'WEB_CLIENT_ID': '907668440978-j9ec27vhg0e0mmpjvrcelfq7ah9n0ntm.apps.googleusercontent.com',
#         'INSTALLED_APP_CLIENT_ID': '907668440978-0ol0griu70qkeb6k3gnn2vipfa5mgl60.apps.googleusercontent.com',
#
#         'DBGAP_AUTHENTICATION_LIST_FILENAME': 'dbGaP_authentication_list',
#         'DBGAP_AUTHENTICATION_LIST_BUCKET': 'isb-cgc-nih-users',
#         'ACL_GOOGLE_GROUP': 'isb-cgc-cntl@isb-cgc.org',
#         'ERA_LOGIN_URL': 'https://104.197.85.205/',
#         'IPV4': '173.194.225.46',
#
#         # Compute services
# 		'PAIRWISE_SERVICE_URL': 'http://104.197.42.216:8080',
#
#         # Cloud Storage Buckets
#         'OPEN_DATA_BUCKET': 'isb-cgc-open',
#         'CONTROLLED_DATA_BUCKET': 'isb-cgc-controlled'
#     }

BQ_PROJECT_ID = SETTINGS['BQ_PROJECT_ID']

# BigQuery cohort storage settings
COHORT_DATASET_ID = SETTINGS['COHORT_DATASET_ID']
DEVELOPER_COHORT_TABLE_ID = SETTINGS['DEVELOPER_COHORT_TABLE_ID']

def get_project_identifier():
    return BQ_PROJECT_ID

BIGQUERY_DATASET = SETTINGS['BIGQUERY_DATASET']
BIGQUERY_DATASET2 = SETTINGS['BIGQUERY_DATASET2']

def get_bigquery_dataset():
    return BIGQUERY_DATASET

BIGQUERY_PROJECT_NAME = SETTINGS['BIGQUERY_PROJECT_NAME']

def get_bigquery_project_name():
    return BIGQUERY_PROJECT_NAME

# Set cohort table here
# if DEVELOPER_COHORT_TABLE_ID is None:
#     raise Exception("Developer-specific cohort table ID is not set.")

class BigQueryCohortStorageSettings(object):
    def __init__(self, dataset_id, table_id):
        self.dataset_id = dataset_id
        self.table_id = table_id

def GET_BQ_COHORT_SETTINGS():
    return BigQueryCohortStorageSettings(COHORT_DATASET_ID, DEVELOPER_COHORT_TABLE_ID)

def get(setting):
    if setting in SETTINGS:
        return SETTINGS[setting]
    else:
        print setting, ' is not a valid setting.'
        return None