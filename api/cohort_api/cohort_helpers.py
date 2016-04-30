
import MySQLdb
import endpoints

from django.conf import settings
from functools import wraps
# from django.db import close_connection


INSTALLED_APP_CLIENT_ID = settings.INSTALLED_APP_CLIENT_ID
CONTROLLED_ACL_GOOGLE_GROUP = settings.ACL_GOOGLE_GROUP


Cohort_Endpoints = endpoints.api(name='cohort_api', version='v1',
                                 description="Get information about cohorts, patients, and samples. Create and delete cohorts.",
                                 allowed_client_ids=[INSTALLED_APP_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])


def cloud_endpoints_close_connection(f):
    # parameter is a list containing a MySQLdb.connections.Connection object and one or more MySQLdb.cursors
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            endpoint = f(*args, **kwargs)
            # close_connection()
            return endpoint
        except:
            # close_connection()
            raise

    return decorated