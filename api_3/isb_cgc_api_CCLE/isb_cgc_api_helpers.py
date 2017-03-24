import endpoints
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

ISB_CGC_CCLE_Endpoints = endpoints.api(name='isb_cgc_ccle_api', version='v3',
                                  description="Get information about cohorts, patients, and samples for CCLE. Create and delete cohorts.",
                                  allowed_client_ids=[INSTALLED_APP_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID,
                                                      settings.WEB_CLIENT_ID],
                                  documentation='http://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/Programmatic-API.html#isb-cgc-api-v3',
                                  title="ISB-CGC API")


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


class CohortsGetListQueryBuilder(object):

    def build_cohort_query(self, query_dict):
        """
        Builds the query that will select cohort id, name, last_date_saved,
        perms, comments, source type, and source notes
        :param query_dict: should contain {'cohorts_cohort_perms.user_id': user_id, 'cohorts_cohort.active': unicode('1')}
        :return: query_str, query_tuple
        
        TODO: see what data migration changes might have occurred to tables in query
        """
        query_str = 'SELECT cohorts_cohort.id, ' \
                    'cohorts_cohort.name, ' \
                    'cohorts_cohort.last_date_saved, ' \
                    'cohorts_cohort_perms.perm, ' \
                    'auth_user.email, ' \
                    'cohorts_cohort_comments.content AS comments, ' \
                    'cohorts_source.type AS source_type, ' \
                    'cohorts_source.notes AS source_notes ' \
                    'FROM cohorts_cohort_perms ' \
                    'JOIN cohorts_cohort ' \
                    'ON cohorts_cohort.id=cohorts_cohort_perms.cohort_id ' \
                    'JOIN auth_user ' \
                    'ON auth_user.id=cohorts_cohort_perms.user_id ' \
                    'LEFT JOIN cohorts_cohort_comments ' \
                    'ON cohorts_cohort_comments.user_id=cohorts_cohort_perms.user_id ' \
                    'AND cohorts_cohort_comments.cohort_id=cohorts_cohort.id ' \
                    'LEFT JOIN cohorts_source ' \
                    'ON cohorts_source.cohort_id=cohorts_cohort_perms.cohort_id '

        query_tuple = ()
        if query_dict:
            query_str += ' WHERE ' + '=%s and '.join(key for key in query_dict.keys()) + '=%s '
            query_tuple = tuple(value for value in query_dict.values())

        query_str += 'GROUP BY ' \
                     'cohorts_cohort.id,  ' \
                     'cohorts_cohort.name,  ' \
                     'cohorts_cohort.last_date_saved,  ' \
                     'cohorts_cohort_perms.perm,  ' \
                     'auth_user.email,  ' \
                     'comments,  ' \
                     'source_type,  ' \
                     'source_notes '

        return query_str, query_tuple

    def build_filter_query(self, filter_query_dict):
        """
        Builds the query that selects the filter name and value for a particular cohort
        :param filter_query_dict: should be {'cohorts_filters.resulting_cohort_id:': id}
        :return: filter_query_str, filter_query_tuple
        
        TODO: see what data migration changes might have occurred to cohorts_filters
        """
        filter_query_str = 'SELECT name, value ' \
                           'FROM cohorts_filters '

        filter_query_str += ' WHERE ' + '=%s AND '.join(key for key in filter_query_dict.keys()) + '=%s '
        filter_query_tuple = tuple(value for value in filter_query_dict.values())

        return filter_query_str, filter_query_tuple

    def build_parent_query(self, parent_query_dict):
        """
        Builds the query that selects parent_ids for a particular cohort
        :param parent_query_dict: should be {'cohort_id': str(row['id'])}
        :return: parent_query_str, parent_query_tuple
        
        TODO: see what data migration changes might have occurred to cohorts_source
        """
        parent_query_str = 'SELECT parent_id ' \
                           'FROM cohorts_source '
        parent_query_str += ' WHERE ' + '=%s AND '.join(key for key in parent_query_dict.keys()) + '=%s '
        parent_query_tuple = tuple(value for value in parent_query_dict.values())

        return parent_query_str, parent_query_tuple

    def build_patients_query(self, patient_query_dict):
        """
        Builds the query that selects the case count for a particular cohort
        :param patient_query_dict: should be {'cohort_id': str(row['id])}
        :return: patient_query_str, patient_query_tuple
        
        TODO: see what data migration changes might have occurred to cohorts_samples
        """
        patients_query_str = 'SELECT case_barcode ' \
                             'FROM cohorts_samples '

        patients_query_str += ' WHERE ' + '=%s AND '.join(key for key in patient_query_dict.keys()) + '=%s '
        patient_query_tuple = tuple(value for value in patient_query_dict.values())

        return patients_query_str, patient_query_tuple

    def build_samples_query(self, sample_query_dict):
        """
        Builds the query that selects the sample count for a particular cohort
        :param sample_query_dict: should be {'cohort_id': str(row['id])}
        :return: sample_query_str, sample_query_tuple
        
        TODO: see what data migration changes might have occurred to cohorts_samples
        """
        samples_query_str = 'SELECT sample_barcode, case_barcode ' \
                            'FROM cohorts_samples '

        samples_query_str += ' WHERE ' + '=%s AND '.join(key for key in sample_query_dict.keys()) + '=%s '
        sample_query_tuple = tuple(value for value in sample_query_dict.values())

        return samples_query_str, sample_query_tuple


class CohortsCreatePreviewQueryBuilder(object):
    def build_query_dictionaries(self, request):
        """
        Builds the query dictionaries for create and preview cohort endpoints.
        Returns query_dict, gte_query_dict, lte_query_dict.
        """
        query_dict = {
            k.name: request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name)
            and k.name is not 'name'
            and not k.name.endswith('_gte')
            and not k.name.endswith('_lte')
            }

        gte_query_dict = {
            k.name.replace('_gte', ''): request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and k.name.endswith('_gte')
            }

        lte_query_dict = {
            k.name.replace('_lte', ''): request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and k.name.endswith('_lte')
            }

        return query_dict, gte_query_dict, lte_query_dict

    def build_query(self, query_dict, gte_query_dict, lte_query_dict):
        """
        Builds the queries that selects the patient and sample barcodes
        that meet the criteria specified in the request body.
        Returns patient query string,  sample query string, value tuple.
        
        TODO: will need to add program parameter to method to add to table name
        """

        patient_query_str = 'SELECT DISTINCT(IF(case_barcode="", LEFT(sample_barcode,12), case_barcode)) ' \
                            'AS case_barcode ' \
                            'FROM metadata_samples ' \
                            'WHERE '

        sample_query_str = 'SELECT sample_barcode, case_barcode ' \
                           'FROM metadata_samples ' \
                           'WHERE '
        value_tuple = ()

        for key, value_list in query_dict.iteritems():
            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            if "None" in value_list:
                value_list.remove("None")
                patient_query_str += ' ( {key} is null '.format(key=key)
                sample_query_str += ' ( {key} is null '.format(key=key)
                if len(value_list) > 0:
                    patient_query_str += ' OR {key} IN ({vals}) '.format(
                        key=key, vals=', '.join(['%s'] * len(value_list)))
                    sample_query_str += ' OR {key} IN ({vals}) '.format(
                        key=key, vals=', '.join(['%s'] * len(value_list)))
                patient_query_str += ') '
                sample_query_str += ') '
            else:
                patient_query_str += ' {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
                sample_query_str += ' {key} IN ({vals}) '.format(key=key, vals=', '.join(['%s'] * len(value_list)))
            value_tuple += tuple(value_list)

        for key, value in gte_query_dict.iteritems():
            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            patient_query_str += ' {} >=%s '.format(key)
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            sample_query_str += ' {} >=%s '.format(key)
            value_tuple += (value,)

        for key, value in lte_query_dict.iteritems():
            patient_query_str += ' AND ' if not patient_query_str.endswith('WHERE ') else ''
            patient_query_str += ' {} <=%s '.format(key)
            sample_query_str += ' AND ' if not sample_query_str.endswith('WHERE ') else ''
            sample_query_str += ' {} <=%s '.format(key)
            value_tuple += (value,)

        sample_query_str += ' GROUP BY sample_barcode'

        return patient_query_str, sample_query_str, value_tuple


class FilterDetails(messages.Message):
    name = messages.StringField(1)
    value = messages.StringField(2)


class CohortsGetListMessageBuilder(object):
    def make_filter_details_from_cursor(self, filter_cursor_dict):
        """
        Returns list of FilterDetails from a dictionary of results
        from a filter query.
        """
        filter_data = []
        for filter_row in filter_cursor_dict:
            filter_data.append(FilterDetails(
                name=str(filter_row['name']),
                value=str(filter_row['value'])
            ))

        if len(filter_data) == 0:
            filter_data.append(FilterDetails(
                name="None",
                value="None"
            ))

        return filter_data

    def make_parent_id_list_from_cursor(self, parent_cursor_dict, row):
        """
        Returns list of parent_id's from a dictionary of results
        from a parent id query.
        """
        parent_id_data = [str(p_row['parent_id']) for p_row in parent_cursor_dict if row.get('parent_id')]
        if len(parent_id_data) == 0:
            parent_id_data.append("None")

        return parent_id_data


class CohortsSamplesFilesQueryBuilder(object):

    def build_query(self, platform=None, pipeline=None, limit=None, cohort_id=None, sample_barcode=None):
        '''
        TODO: will need to add program and genomic build to method to add to metadata_data, check changes to cohorts_samples
        '''
        query_str = 'SELECT DataFileNameKey, SecurityProtocol, Repository ' \
                    'FROM metadata_data '

        if cohort_id is None:
            query_str += 'WHERE sample_barcode=%s '
        else:
            query_str += 'JOIN cohorts_samples ON metadata_data.sample_barcode=cohorts_samples.sample_barcode ' \
                         'WHERE cohorts_samples.cohort_id=%s '

        query_str += 'AND DataFileNameKey != "" AND DataFileNameKey is not null '
        query_str += ' and metadata_data.Platform=%s ' if platform is not None else ''
        query_str += ' and metadata_data.Pipeline=%s ' if pipeline is not None else ''
        query_str += ' GROUP BY DataFileNameKey, SecurityProtocol, Repository '
        query_str += ' LIMIT %s' if limit is not None else ' LIMIT 10000'

        query_tuple = (cohort_id,) if cohort_id is not None else (sample_barcode,)
        query_tuple += (platform,) if platform is not None else ()
        query_tuple += (pipeline,) if pipeline is not None else ()
        query_tuple += (limit,) if limit is not None else ()

        return query_str, query_tuple


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
            if not row.get('DataFileNameKey'):
                continue

            if 'controlled' not in str(row['SecurityProtocol']).lower():
                # this may only be necessary for the vagrant db
                path = row.get('DataFileNameKey') if row.get('DataFileNameKey') is None \
                    else row.get('DataFileNameKey').replace('gs://' + settings.OPEN_DATA_BUCKET, '')
                row['cloud_storage_path'] = "gs://{}{}".format(settings.OPEN_DATA_BUCKET, path)
            else:
                if row['Repository'].lower() == 'dcc':
                    bucket_name = settings.DCC_CONTROLLED_DATA_BUCKET
                elif row['Repository'].lower() == 'cghub':
                    bucket_name = settings.CGHUB_CONTROLLED_DATA_BUCKET
                else:
                    bad_repo_count += 1
                    bad_repo_set.add(row['Repository'])
                    continue
                # this may only be necessary for the vagrant db
                path = row.get('DataFileNameKey') if row.get('DataFileNameKey') is None \
                    else row.get('DataFileNameKey').replace('gs://' + bucket_name, '')

                row['cloud_storage_path'] = "gs://{}{}".format(bucket_name, path)
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