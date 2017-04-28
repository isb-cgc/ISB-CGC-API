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
from collections import OrderedDict
import logging
import MySQLdb

try:
    import endpoints
except Exception as e:
    print 'couldn\'t import google endpoints, using mock for testing: %s' % (e)
import django

from django.conf import settings
from django.core.signals import request_finished
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from sharing.models import User
# from django.contrib.auth.models import User as Django_User
try:
    from protorpc import remote, messages
except Exception as e:
    print 'couldn\'t import google protorpc, using mock for testing: %s' % (e)

from api_3.api_helpers import sql_connection
from cohorts.models import Cohort as Django_Cohort, Cohort_Perms

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL

class GCSFilePathList(messages.Message):
    cloud_storage_file_paths = messages.StringField(1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)


class CloudStorageFilePathsAPI(remote.Service):
    def setup_param_map(self, request, param_names):
        param_map = OrderedDict()
        for param_name in param_names:
            param_map[param_name] = request.get_assigned_value(param_name)
        return param_map


    def get_genomic_builds(self, param_map):
        builds = ['HG19', 'HG38']
        if 'genomic_build' in param_map and param_map['genomic_build']:
            if 'HG19' == param_map['genomic_build'].upper():
                builds = ['HG19']
            elif 'HG38' == param_map['genomic_build'].upper():
                builds = ['HG38']
            else:
                msg = 'Unknown genomic build: {}.  Acceptable genomic builds are HG19 and HG38.'.format(param_map['genomic_build'])
                logger.warn(msg)
                raise endpoints.BadRequestException("Error retrieving genomics data for cohort. {}".format(msg))
        return builds

    def build_query(self, param_map, program):
        builds = self.get_genomic_builds(param_map)
        final_query_str = ''
        query_tuple = []
        for build in builds:
            query_str = 'SELECT md.file_name_key, md.access ' \
                        'FROM {}_metadata_data_{} md '.format(program, build)
    
            if 'sample_barcode' in param_map:
                query_str += 'WHERE sample_barcode=%s '
                query_tuple += [param_map['sample_barcode']]
            else:
                query_str += 'JOIN cohorts_samples cs ON md.sample_barcode=cs.sample_barcode ' \
                             'WHERE cs.cohort_id=%s '
                query_tuple += [param_map['cohort_id']]
            query_str += 'AND file_name_key != "" AND file_name_key is not null '
            for field, value in param_map.iteritems():
                if  field not in ['limit', 'cohort_id', 'sample_barcode', 'genomic_build'] and value:
                    query_str += ' and md.{}=%s '.format(field)
                    query_tuple += [value]
            query_str += ' GROUP BY md.file_name_key, md.access '
            if 0 < len(final_query_str):
                final_query_str += ' UNION '
            final_query_str += query_str
        
        if 'limit' in param_map and param_map['limit']:
            query_str += ' LIMIT %s'  
            query_tuple += [param_map['limit']]
        else:
            query_str += ' LIMIT 10000'
        return final_query_str, query_tuple

    def get_cloud_storage_file_paths(self, param_map, program):
        """
        Uses the param_map to pass to the query builder then executes the query to obtain the cloud
        storage file paths.  if cohort_id is on the parameter list, verifies that the calling user has
        permission for the cohort. 
        """
        cursor = None
        db = None

        query_str, query_tuple = self.build_query(param_map, program)

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)
            cursor_rows = cursor.fetchall()
            cloud_storage_path_list = [row['file_name_key'] for row in cursor_rows]
            return GCSFilePathList(cloud_storage_file_paths=cloud_storage_path_list, count=len(cloud_storage_path_list))
        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException("File paths for cohort {} not found.\nSQL: {}\nparams: {}" \
                            .format(param_map['cohort_id'] if 'cohort_id' in param_map else param_map['sample_barcode'], query_str, query_tuple))
        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving file paths. {}".format(e))
            raise endpoints.BadRequestException("Error retrieving file paths. {}".format(e))
        finally:
            if cursor: 
                cursor.close()
            if db and db.open: 
                db.close()

class SamplesCloudStorageFilePathsHelper(CloudStorageFilePathsAPI):

    GET_RESOURCE = endpoints.ResourceContainer(
        sample_barcode=messages.StringField(1, required=True),
        data_type=messages.StringField(2),
        data_category=messages.StringField(3),
        experimental_strategy=messages.StringField(4),
        data_format=messages.StringField(5),
        platform=messages.StringField(6),
        genomic_build=messages.StringField(7),
        analysis_workflow_type=messages.StringField(8)
    )

    def cloud_storage_file_paths(self, request, program):
        param_map = self.setup_param_map(request, [
                'data_type', 
                'data_category', 
                'experimental_strategy', 
                'data_format', 
                'platform', 
                'genomic_build', 
                'analysis_workflow_type', 
                'sample_barcode'
            ]
        )
        return self.get_cloud_storage_file_paths(param_map, program)
    
class CohortsCloudStorageFilePathsHelper(CloudStorageFilePathsAPI):

    GET_RESOURCE = endpoints.ResourceContainer(
        cohort_id=messages.IntegerField(1, required=True),
        limit=messages.IntegerField(2),
        data_type=messages.StringField(3),
        data_category=messages.StringField(4),
        experimental_strategy=messages.StringField(5),
        data_format=messages.StringField(6),
        platform=messages.StringField(7),
        genomic_build=messages.StringField(8),
        analysis_workflow_type=messages.StringField(9)
    )

    def validate_user(self, cohort_id):
        user_email = None
        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register "
                "with the web application.".format(BASE_URL))

        django.setup()
        try:
            user_id = User.objects.get(email=user_email).id
            Django_Cohort.objects.get(id=cohort_id)
            Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user_id)
        except (ObjectDoesNotExist, MultipleObjectsReturned), e:
            logger.warn(e)
            err_msg = "Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e)
            if 'Cohort_Perms' in e.message:
                err_msg = "User {} does not have permissions on cohort {}.".format(user_email, cohort_id)
            raise endpoints.UnauthorizedException(err_msg)
        finally:
            request_finished.send(self)
    
    def cloud_storage_file_paths(self, request, program):
        param_map = self.setup_param_map(request, [
                'data_type', 
                'data_category', 
                'experimental_strategy', 
                'data_format', 
                'platform', 
                'genomic_build', 
                'analysis_workflow_type', 
                'limit', 
                'cohort_id'
            ]
        )
        self.validate_user(param_map['cohort_id'])
        return self.get_cloud_storage_file_paths(param_map, program)
