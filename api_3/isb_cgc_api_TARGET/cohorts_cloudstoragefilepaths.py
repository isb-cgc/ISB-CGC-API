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

import endpoints
import logging
import MySQLdb
import django

from django.conf import settings
from django.core.signals import request_finished
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_TARGET_Endpoints, CohortsSamplesFilesQueryBuilder, CohortsSamplesFilesMessageBuilder
from api_3.api_helpers import sql_connection
from cohorts.models import Cohort as Django_Cohort, Cohort_Perms

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class GCSFilePathList(messages.Message):
    cloud_storage_file_paths = messages.StringField(1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)


@ISB_CGC_TARGET_Endpoints.api_class(resource_name='cohorts')
class CohortsCloudStorageFilePathsAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True),
                                               limit=messages.IntegerField(2),
                                               platform=messages.StringField(3),
                                               pipeline=messages.StringField(4))

    @endpoints.method(GET_RESOURCE, GCSFilePathList,  http_method='GET',
                      path='cohorts/{cohort_id}/cloud_storage_file_paths')
    def cloud_storage_file_paths(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        user_email = None
        cursor = None
        db = None

        limit = request.get_assigned_value('limit')
        platform = request.get_assigned_value('platform')
        pipeline = request.get_assigned_value('pipeline')
        cohort_id = request.get_assigned_value('cohort_id')

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register "
                "with the web application.".format(BASE_URL))

        django.setup()
        try:
            user_id = Django_User.objects.get(email=user_email).id
            Django_Cohort.objects.get(id=cohort_id)
            Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user_id)
        except (ObjectDoesNotExist, MultipleObjectsReturned), e:
            logger.warn(e)
            err_msg = "Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e)
            if 'Cohort_Perms' in e.message:
                err_msg = "User {} does not have permissions on cohort {}. " \
                          "Error: {}".format(user_email, cohort_id, e)
            raise endpoints.UnauthorizedException(err_msg)
        finally:
            request_finished.send(self)

        query_str, query_tuple = CohortsSamplesFilesQueryBuilder().build_query(
            platform=platform, pipeline=pipeline, limit=limit, cohort_id=cohort_id)

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)
            cursor_rows = cursor.fetchall()
            bad_repo_count, bad_repo_set = CohortsSamplesFilesMessageBuilder().get_GCS_file_paths_and_bad_repos(cursor_rows)
            cloud_storage_path_list = [row['cloud_storage_path'] for row in cursor_rows]
            if bad_repo_count > 0:
                logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                            .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))
            return GCSFilePathList(cloud_storage_file_paths=cloud_storage_path_list, count=len(cloud_storage_path_list))

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException("File paths for cohort {} not found.".format(cohort_id))
        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving file paths. {}".format(e))
            raise endpoints.BadRequestException("Error retrieving file paths. {}".format(e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()