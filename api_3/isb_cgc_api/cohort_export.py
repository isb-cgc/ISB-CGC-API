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


class CohortFilters(messages.Message):
    program = messages.StringField(1, repeated=True)
    disease_code = messages.StringField(2, repeated=True)
    project_short_name = messages.StringField(8, repeated=True)


class CohortExportResult(messages.Message):
    message = messages.StringField(2),
    export_dest = messages.StringField(1),
    num_exported = message.IntegerField(3)


class ExportDestinationType(messages.Enum):
    BIG_QUERY=1,
    CLOUD_STORAGE=2


class ExportCohort(remote.Service):
    POST_RESOURCE = endpoints.ResourceContainer(
        cohort_id=messages.IntegerField(1, required=True),
        filters=messages.MessageField(CohortFilters, 2),
        destination_type=messages.EnumField(ExportDestinationType, 4, required=True),
        destination=messages.StringField(3, required=True),
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

    def export_cohort_file_manifest(self, request):
        cohort_id = request.get_assigned_value('cohort_id')
        export_result = CohortExportResult()

        try:
            user = self.validate_user(cohort_id)

            filter_obj = request.get_assigned_value('filters') if 'filters' in [k.name for k in request.all_fields()] else None

            inc_filters = {
                filter.name: filter_obj.get_assigned_value(filter.name)
                           for filter in filter_obj.all_fields()
                           if filter_obj.get_assigned_value(filter.name)
                } if filter_obj else {}

            # Call export method

        except Exception as e:
            logger.exception(e)
            raise endpoints.InternalServerErrorException("There was an error while processing your request.")

        return export_result

    def export_cohort(self, request):
        cohort_id = request.get_assigned_value('cohort_id')
        export_result = CohortExportResult()

        try:
            user = self.validate_user(cohort_id)

            filter_obj = request.get_assigned_value('filters') if 'filters' in [k.name for k in request.all_fields()] else None

            inc_filters = {
                filter.name: filter_obj.get_assigned_value(filter.name)
                           for filter in filter_obj.all_fields()
                           if filter_obj.get_assigned_value(filter.name)
                } if filter_obj else {}

            # Call export method

        except Exception as e:
            logger.exception(e)
            raise endpoints.InternalServerErrorException("There was an error while processing your request.")

        return export_result


@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortExportAPI(ExportCohort):

    @endpoints.method(ExportCohort.POST_RESOURCE, CohortExportResult, http_method='POST', path='cohorts/{cohort_id}/export')
    def export_cohort(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        return super(CohortExportAPI, self).export_cohort(request)

@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortExportFileManifestAPI(ExportCohort):

    @endpoints.method(ExportCohort.POST_RESOURCE, CohortExportResult, http_method='POST', path='cohorts/{cohort_id}/export/file_manifest')
    def export_cohort_file_manifest(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        return super(CohortExportFileManifestAPI, self).export_cohort_file_manifest(request)