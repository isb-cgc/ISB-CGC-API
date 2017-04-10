"""

Copyright 2017, Institute for Systems Biology

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
from django.conf import settings
from protorpc import messages
import logging

logger = logging.getLogger(__name__)

INSTALLED_APP_CLIENT_ID = settings.INSTALLED_APP_CLIENT_ID
CONTROLLED_ACL_GOOGLE_GROUP = settings.ACL_GOOGLE_GROUP

BUILTIN_ENDPOINTS_PARAMETERS = [
    'alt',
    'fields',
    'enum',
    'enumDescriptions',
    'key',
    'oauth_token',
    'prettyPrint',
    'quotaUser',
    'userIp'
]

def are_there_bad_keys(request):
    '''
    Checks for unrecognized fields in an endpoint request
    :param request: the request object from the endpoint
    :return: boolean indicating True if bad (unrecognized) fields are present in the request
    '''
    unrecognized_param_dict = {
        k: request.get_unrecognized_field_info(k)[0]
        for k in request.all_unrecognized_fields()
        if k not in BUILTIN_ENDPOINTS_PARAMETERS
        }
    return unrecognized_param_dict != {}


def are_there_no_acceptable_keys(request):
    """
    Checks for a lack of recognized fields in an endpoints request. Used in save_cohort and preview_cohort endpoints.
    :param request: the request object from the endpoint
    :return: boolean indicating True if there are no recognized fields in the request.
    """
    param_dict = {
        k.name: request.get_assigned_value(k.name)
        for k in request.all_fields()
        if request.get_assigned_value(k.name)
        }
    return param_dict == {}


def construct_parameter_error_message(request, filter_required):
    err_msg = ''
    sorted_acceptable_keys = sorted([k.name for k in request.all_fields()], key=lambda s: s.lower())
    unrecognized_param_dict = {
        k: request.get_unrecognized_field_info(k)[0]
        for k in request.all_unrecognized_fields()
        if k not in BUILTIN_ENDPOINTS_PARAMETERS
        }
    if unrecognized_param_dict:
        bad_key_str = "'" + "', '".join(unrecognized_param_dict.keys()) + "'"
        err_msg += "The following filters were not recognized: {}. ".format(bad_key_str)
    if filter_required:
        err_msg += "You must specify at least one of the following " \
                   "case-sensitive filters: {}".format(sorted_acceptable_keys)
    else:
        err_msg += "Acceptable filters are: {}".format(sorted_acceptable_keys)

    return err_msg


class FilterDetails(messages.Message):
    name = messages.StringField(1)
    value = messages.StringField(2)

class CohortsSamplesFilesMessageBuilder(object):

    def get_GCS_file_paths_and_bad_repos(self, cursor_rows):
        """
         Used in cohorts.datafilenamekeys, samples.datafilenamekeys, samples.get.
        Modifies cursor_rows to add the cloud storage path to each row representing a file.
        A count of bad repositories and a set of bad repositories is returned in case
        there are any errors with the data repository information in the row.
        :param cursor_rows: list of dictionaries resulting from a database query.
        Each dictionary with the key 'DataFileNameKey' must also have a 'SecurityProtocol' key.
        Each dictionary with 'controlled' in the value for 'SecurityProtocol' must also
        have the key 'Repository'.
        :return: bad_repo_count, bad_repo_set

        TODO: update DataFileNameKey to file_name_key
        """
        bad_repo_count = 0
        bad_repo_set = set()
        for row in cursor_rows:
            if not row.get('file_name_key'):
                continue
            row['cloud_storage_path'] = row.get('file_name_key')
        return bad_repo_count, bad_repo_set


def build_constructor_dict_for_message(message_class, row):
    """
    Takes an instance of a message class and a dictionary of values from a database query
    and first validates the values in the dictionary against the message class fields
    and then returns a dictionary of all the validated key-value pairs in the database query.
    This will only work if the headers in the database query have the same name as the names of
    fields in the message class.
    """
    constructor_dict = {}
    metadata_item_dict = {field.name: field for field in message_class.all_fields()}
    for name, field in metadata_item_dict.iteritems():
        if row.get(name) is not None:
            try:
                field.validate(row[name])
                constructor_dict[name] = row[name]
            except messages.ValidationError, e:
                constructor_dict[name] = None
                logger.warn('{name}: {value} was not validated while constructing kwargs for {message_class}. Error: {e}'
                            .format(name=name, value=str(row[name]), message_class=str(message_class), e=e))
        else:
            constructor_dict[name] = None

    return constructor_dict
