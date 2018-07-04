"""

Copyright 2018, Institute for Systems Biology

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
import django
from protorpc import remote, messages

from django.core.signals import request_finished
from django.contrib.auth.models import User as Django_User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings

from api_3.isb_cgc_api.isb_cgc_api_helpers import ISB_CGC_Endpoints

from cohorts.file_helpers import cohort_files
from cohorts.models import Cohort_Perms
from accounts.sa_utils import auth_dataset_whitelists_for_user

BASE_URL = settings.BASE_URL

logger = logging.getLogger(__name__)


class FileDetail(messages.Message):
    program = messages.StringField(1, required=True)
    case_barcode = messages.StringField(2, required=True)
    file_path = messages.StringField(3, required=True)
    file_gdc_uuid = messages.StringField(4)
    disease_code = messages.StringField(5, required=True)
    experimental_strategy = messages.StringField(6)
    platform = messages.StringField(7)
    data_category = messages.StringField(8)
    data_type = messages.StringField(9)
    data_format = messages.StringField(10)
    access = messages.StringField(11)
    case_gdc_uuid = messages.StringField(12)
    project_short_name = messages.StringField(13)


class FileManifest(messages.Message):
    files = messages.MessageField(FileDetail, 1, repeated=True)
    total_file_count = messages.IntegerField(2, variant=messages.Variant.INT32)
    files_retrieved = messages.IntegerField(3, variant=messages.Variant.INT32)


class FileManifestFilters(messages.Message):
    program = messages.StringField(1, repeated=True)
    disease_code = messages.StringField(2, repeated=True)
    experimental_strategy = messages.StringField(3, repeated=True)
    platform = messages.StringField(4, repeated=True)
    data_category = messages.StringField(5, repeated=True)
    data_type = messages.StringField(6, repeated=True)
    data_format = messages.StringField(7, repeated=True)
    project_short_name = messages.StringField(8, repeated=True)


class CohortFileManifest(remote.Service):
    GET_RESOURCE = endpoints.ResourceContainer(
        cohort_id=messages.IntegerField(1, required=True),
        fetch_count=messages.IntegerField(2),
        offset=messages.IntegerField(3),
        genomic_build=messages.StringField(4),
        do_filter_count=messages.BooleanField(6)
    )

    POST_RESOURCE = endpoints.ResourceContainer(
        cohort_id=messages.IntegerField(1, required=True),
        fetch_count=messages.IntegerField(2),
        offset=messages.IntegerField(3),
        genomic_build=messages.StringField(4),
        do_filter_count=messages.BooleanField(6),
        filters=messages.MessageField(FileManifestFilters, 5)
    )

    def validate_user(self, cohort_id):
        user_email = None
        user = None
        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()
        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register "
                "with the web application.".
                format(BASE_URL))
        django.setup()
        try:
            user = Django_User.objects.get(email=user_email)
            Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user.id)
        except ObjectDoesNotExist as e:
            err_msg = "Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e)
            if 'Cohort_Perms' in e.message:
                err_msg = "User {} does not have permissions on cohort {}.".format(user_email, cohort_id)
            logger.exception(e)
            raise endpoints.UnauthorizedException(err_msg)
        finally:
            request_finished.send(self)
        return user

    def file_manifest(self, request):
        cohort_id = request.get_assigned_value('cohort_id')
        file_manifest = None

        try:
            user = self.validate_user(cohort_id)
            has_access = auth_dataset_whitelists_for_user(user.id)

            params = {}

            if request.get_assigned_value('offset'):
                params['offset'] = request.get_assigned_value('offset')

            if request.get_assigned_value('fetch_count'):
                params['limit'] = request.get_assigned_value('fetch_count')
            else:
                params['limit'] = settings.MAX_FILE_LIST_REQUEST

            if request.get_assigned_value('do_filter_count'):
                params['do_filter_count'] = request.get_assigned_value('do_filter_count')

            params['access'] = has_access

            filter_obj = request.get_assigned_value('filters') if 'filters' in [k.name for k in request.all_fields()] else None

            inc_filters = {
                filter.name: filter_obj.get_assigned_value(filter.name)
                           for filter in filter_obj.all_fields()
                           if filter_obj.get_assigned_value(filter.name)
                } if filter_obj else {}

            response = cohort_files(cohort_id, user=user, inc_filters=inc_filters, **params)

            file_manifest = FileManifest()
            files = []

            for file in response['file_list']:
                files.append(FileDetail(
                    program=file['program'],
                    case_barcode=file['case'],
                    case_gdc_uuid=file['case_gdc_id'],
                    file_path=file['cloudstorage_location'],
                    file_gdc_uuid=file['file_gdc_id'],
                    disease_code=file['disease_code'],
                    project_short_name=file['project_short_name'],
                    experimental_strategy=file['exp_strat'],
                    platform=file['platform'],
                    data_category=file['datacat'],
                    data_type=file['datatype'],
                    data_format=file['dataformat'],
                    access=file['access']
                ))

            file_manifest.files = files
            file_manifest.total_file_count = response['total_file_count']
            file_manifest.files_retrieved = len(files)

        except Exception as e:
            logger.exception(e)
            raise endpoints.InternalServerErrorException("There was an error while processing your request.")

        return file_manifest


@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortFileManifestAPI(CohortFileManifest):

    @endpoints.method(CohortFileManifest.GET_RESOURCE, FileManifest, http_method='GET', path='cohorts/{cohort_id}/file_manifest')
    def file_manifest(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        return super(CohortFileManifestAPI, self).file_manifest(request)

    @endpoints.method(CohortFileManifest.POST_RESOURCE, FileManifest, http_method='POST', path='cohorts/{cohort_id}/file_manifest')
    def file_manifest_filtered(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        return super(CohortFileManifestAPI, self).file_manifest(request)
