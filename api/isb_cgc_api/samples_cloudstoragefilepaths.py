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

from django.conf import settings
from django.core.signals import request_finished
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints, are_there_bad_keys, construct_parameter_error_message, \
    CohortsSamplesFilesQueryBuilder, CohortsSamplesFilesMessageBuilder
from api.api_helpers import sql_connection

logger = logging.getLogger(__name__)


class GCSFilePathList(messages.Message):
    cloud_storage_file_paths = messages.StringField(1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)


@ISB_CGC_Endpoints.api_class(resource_name='samples')
class SamplesCloudStorageFilePathsAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True),
                                               platform=messages.StringField(2),
                                               pipeline=messages.StringField(3))

    @endpoints.method(GET_RESOURCE, GCSFilePathList,
                      path='samples/{sample_barcode}/cloud_storage_file_paths', http_method='GET')
    def cloud_storage_file_paths(self, request):
        """
        Takes a sample barcode as a required parameter and
        returns cloud storage paths to files associated with that sample.
        """
        cursor = None
        db = None

        sample_barcode = request.get_assigned_value('sample_barcode')
        platform = request.get_assigned_value('platform')
        pipeline = request.get_assigned_value('pipeline')

        if are_there_bad_keys(request):
            err_msg = construct_parameter_error_message(request, False)
            raise endpoints.BadRequestException(err_msg)

        query_str, query_tuple = CohortsSamplesFilesQueryBuilder().build_query(
            platform=platform, pipeline=pipeline, sample_barcode=sample_barcode)

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)
            cursor_rows = cursor.fetchall()
            # add 'cloud_storage_path' to cursor_rows
            bad_repo_count, bad_repo_set = CohortsSamplesFilesMessageBuilder().get_GCS_file_paths_and_bad_repos(cursor_rows)
            cloud_storage_path_list = [row['cloud_storage_path'] for row in cursor_rows]
            if bad_repo_count > 0:
                logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                            .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))
            return GCSFilePathList(cloud_storage_file_paths=cloud_storage_path_list, count=len(cloud_storage_path_list))

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException("File paths for sample {} not found.".format(sample_barcode))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\t query: {} {}'.format(e, query_str, query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving file paths. {}".format(msg))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)