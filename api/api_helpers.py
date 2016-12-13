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

import sys
import os
import MySQLdb
import httplib2
from oauth2client.client import GoogleCredentials, AccessTokenCredentials
from django.conf import settings
from googleapiclient.discovery import build

CONTROLLED_ACL_GOOGLE_GROUP = settings.ACL_GOOGLE_GROUP
debug = settings.DEBUG

WHITELIST_RE = ur'([^\\\_\|\"\+~@:#\$%\^&\*=\-\.,\(\)0-9a-zA-Z\s\xc7\xfc\xe9\xe2\xe4\xe0\xe5\xe7\xea\xeb\xe8\xef\xee\xed\xec\xc4\xc5\xc9\xe6\xc6\xf4\xf6\xf2\xfb\xf9\xd6\xdc\xe1\xf3\xfa\xf1\xd1\xc0\xc1\xc2\xc3\xc8\xca\xcb\xcc\xcd\xce\xcf\xd0\xd2\xd3\xd4\xd5\xd8\xd9\xda\xdb\xdd\xdf\xe3\xf0\xf5\xf8\xfd\xfe\xff])'

MOLECULAR_CATEGORIES = {
    'nonsilent': [
        'Missense_Mutation',
        'Nonsense_Mutation',
        'Nonstop_Mutation',
        'Frame_Shift_Del',
        'Frame_Shift_Ins',
        'De_novo_Start_OutOfFrame',
        'In_Frame_Del',
        'In_Frame_Ins',
        'Start_Codon_SNP',
        'Start_Codon_Del',
    ]
}

# Database connection
def sql_connection():
    env = os.getenv('SERVER_SOFTWARE')
    database = settings.DATABASES['default']
    if env.startswith('Google App Engine/'):
        # Connecting from App Engine
        try:
            db = MySQLdb.connect(
                unix_socket = database['HOST'],
                # port = 3306,
                db=database['NAME'],
                user=database['USER'],
                passwd=database['PASSWORD'],
                ssl=database['OPTIONS']['ssl'])
        except:
            print >> sys.stderr, "Unexpected ERROR in sql_connection(): ", sys.exc_info()[0]
            #return HttpResponse( traceback.format_exc() )
            raise # if you want to soldier bravely on despite the exception, but comment to stderr
    else:
        try:
            connect_options = {
                'host': database['HOST'],
                'db': database['NAME'],
                'user': database['USER'],
                'passwd': database['PASSWORD']
            }

            if 'OPTIONS' in database and 'ssl' in database['OPTIONS']:
                connect_options['ssl'] = database['OPTIONS']['ssl']

            db = MySQLdb.connect(**connect_options)
        except:
            print >> sys.stderr, "Unexpected ERROR in sql_connection(): ", sys.exc_info()[0]
            #return HttpResponse( traceback.format_exc() )
            raise # if you want to soldier bravely on despite the exception, but comment to stderr

    return db


def sql_bmi_by_ranges(value):
    if debug: print >> sys.stderr, 'Called ' + sys._getframe().f_code.co_name
    result = ''
    if not isinstance(value, basestring):
        # value is a list of ranges
        first = True
        if 'None' in value:
            result += 'BMI is null or '
            value.remove('None')
        for val in value:
            if first:
                result += ''
                first = False
            else:
                result += ' or'
            if str(val) == 'underweight':
                result += ' (BMI < 18.5)'
            elif str(val) == 'normal weight':
                result += ' (BMI >= 18.5 and BMI <= 24.9)'
            elif str(val) == 'overweight':
                result += ' (BMI > 24.9 and BMI <= 29.9)'
            elif str(val) == 'obese':
                result += ' (BMI > 29.9)'

    else:
        # value is a single range
        if str(value) == 'underweight':
            result += ' (BMI < 18.5)'
        elif str(value) == 'normal weight':
            result += ' (BMI >= 18.5 and BMI <= 24.9)'
        elif str(value) == 'overweight':
            result += ' (BMI > 24.9 and BMI <= 29.9)'
        elif str(value) == 'obese':
            result += ' (BMI > 29.9)'

    return result


def sql_age_by_ranges(value):
    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    result = ''
    if not isinstance(value, basestring):
        #value is a list of ranges
        first = True
        if 'None' in value:
            result += 'age_at_initial_pathologic_diagnosis is null or '
            value.remove('None')
        for val in value:
            if first:
                result += ''
                first = False
            else:
                result += ' or'
            if str(val) == '10 to 39':
                result += ' (age_at_initial_pathologic_diagnosis >= 10 and age_at_initial_pathologic_diagnosis < 40)'
            elif str(val) == '40 to 49':
                result += ' (age_at_initial_pathologic_diagnosis >= 40 and age_at_initial_pathologic_diagnosis < 50)'
            elif str(val) == '50 to 59':
                result += ' (age_at_initial_pathologic_diagnosis >= 50 and age_at_initial_pathologic_diagnosis < 60)'
            elif str(val) == '60 to 69':
                result += ' (age_at_initial_pathologic_diagnosis >= 60 and age_at_initial_pathologic_diagnosis < 70)'
            elif str(val) == '70 to 79':
                result += ' (age_at_initial_pathologic_diagnosis >= 70 and age_at_initial_pathologic_diagnosis < 80)'
            elif str(val).lower() == 'over 80':
                result += ' (age_at_initial_pathologic_diagnosis >= 80)'
    else:
        #value is a single range
        if str(value) == '10 to 39':
            result += ' (age_at_initial_pathologic_diagnosis >= 10 and age_at_initial_pathologic_diagnosis < 40)'
        elif str(value) == '40 to 49':
            result += ' (age_at_initial_pathologic_diagnosis >= 40 and age_at_initial_pathologic_diagnosis < 50)'
        elif str(value) == '50 to 59':
            result += ' (age_at_initial_pathologic_diagnosis >= 50 and age_at_initial_pathologic_diagnosis < 60)'
        elif str(value) == '60 to 69':
            result += ' (age_at_initial_pathologic_diagnosis >= 60 and age_at_initial_pathologic_diagnosis < 70)'
        elif str(value) == '70 to 79':
            result += ' (age_at_initial_pathologic_diagnosis >= 70 and age_at_initial_pathologic_diagnosis < 80)'
        elif str(value).lower() == 'over 80':
            result += ' (age_at_initial_pathologic_diagnosis >= 80)'
        elif str(value) == 'None':
            result += ' age_at_initial_pathologic_diagnosis is null'

    return result

def gql_age_by_ranges(q, key, value):
    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    result = ''
    if not isinstance(value, basestring):
        # value is a list of ranges
        first = True
        for val in value:
            if first:
                first = False
            else:
                result += ' or'
            if str(val) == '10to39':
                result += ' (%s >= 10 and %s < 40)' % (key, key)
            elif str(val) == '40to49':
                result += ' (%s >= 40 and %s < 50)' % (key, key)
            elif str(val) == '50to59':
                result += ' (%s >= 50 and %s < 60)' % (key, key)
            elif str(val) == '60to69':
                result += ' (%s >= 60 and %s < 70)' % (key, key)
            elif str(val) == '70to79':
                result += ' (%s >= 70 and %s < 80)' % (key, key)
            elif str(val).lower() == 'over80':
                result += ' (%s >= 80)' % key
    else:
        # value is a single range
        if str(value) == '10to39':
            result += ' (%s >= 10 and %s < 40)' % (key, key)
        elif str(value) == '40to49':
            result += ' (%s >= 40 and %s < 50)' % (key, key)
        elif str(value) == '50to59':
            result += ' (%s >= 50 and %s < 60)' % (key, key)
        elif str(value) == '60to69':
            result += ' (%s >= 60 and %s < 70)' % (key, key)
        elif str(value) == '70to79':
            result += ' (%s >= 70 and %s < 80)' % (key, key)
        elif str(value).lower() == 'over80':
            result += ' (%s >= 80)' % key
    return result


def normalize_bmi(bmis):
    if debug: print >> sys.stderr, 'Called ' + sys._getframe().f_code.co_name
    bmi_list = {'underweight': 0, 'normal weight': 0, 'overweight': 0, 'obese': 0, 'None': 0}
    for bmi, count in bmis.items():
        if type(bmi) != dict:
            if bmi and bmi != 'None':
                fl_bmi = float(bmi)
                if fl_bmi < 18.5:
                    bmi_list['underweight'] += int(count)
                elif 18.5 <= fl_bmi <= 24.9:
                    bmi_list['normal weight'] += int(count)
                elif 25 <= fl_bmi <= 29.9:
                    bmi_list['overweight'] += int(count)
                elif fl_bmi >= 30:
                    bmi_list['obese'] += int(count)
            else:
                bmi_list['None'] += int(count)

    return bmi_list


def normalize_ages(ages):
    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    new_age_list = {'10 to 39': 0, '40 to 49': 0, '50 to 59': 0, '60 to 69': 0, '70 to 79': 0, 'Over 80': 0, 'None': 0}
    for age, count in ages.items():
        if type(age) != dict:
            if age and age != 'None':
                int_age = float(age)
                if int_age < 40:
                    new_age_list['10 to 39'] += int(count)
                elif int_age < 50:
                    new_age_list['40 to 49'] += int(count)
                elif int_age < 60:
                    new_age_list['50 to 59'] += int(count)
                elif int_age < 70:
                    new_age_list['60 to 69'] += int(count)
                elif int_age < 80:
                    new_age_list['70 to 79'] += int(count)
                else:
                    new_age_list['Over 80'] += int(count)
            else:
                new_age_list['None'] += int(count)
        else:
            print age

    return new_age_list

def applyFilter(field, dict):
# this one gets called a lot...
#    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    query_dict = dict.copy()
    if field in dict:
        query_dict.pop(field, None)
        if len(query_dict) > 0:
            where_clause = build_where_clause(query_dict)
        else:
            where_clause = None
    else:
        where_clause = build_where_clause(dict)

    return where_clause


def build_where_clause(filters, alt_key_map=False):
# this one gets called a lot
#    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    first = True
    query_str = ''
    big_query_str = ''  # todo: make this work for non-string values -- use {}.format
    value_tuple = ()
    key_order = []
    keyType = None
    gene = None

    grouped_filters = None

    for key, value in filters.items():
        if isinstance(value, dict) and 'values' in value:
            value = value['values']

        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        # Check if we need to map to a different column name for a given key
        if alt_key_map and key in alt_key_map:
            key = alt_key_map[key]

        # Multitable where's will come in with : in the name. Only grab the column piece for now
        # TODO: Shouldn't throw away the entire key
        elif ':' in key:
            keyType = key.split(':')[0]
            if keyType == 'MUT':
                gene = key.split(':')[1]
            key = key.split(':')[-1]

        # Multitable filter lists don't come in as string as they can contain arbitrary text in values
        elif isinstance(value, basestring):
            # If it's a list of values, split it into an array
            if ',' in value:
                value = value.split(',')

        key_order.append(key)

        # Bucket the grouped filter types (currently just certain has_ values, could be more)
        if 'has_' in key and not key == 'has_Illumina_DNASeq' and not key == 'has_SNP6' and not key == 'has_RPPA':
            if grouped_filters is None:
                grouped_filters = {}

            if key == 'has_27k' or key == 'has_450k':
                if 'DNA_methylation' not in grouped_filters:
                    grouped_filters['DNA_methylation'] = []
                grouped_filters['DNA_methylation'].append({'filter': str(key), 'value': str(value)})
            elif key == 'has_HiSeq_miRnaSeq' or key == 'has_GA_miRNASeq':
                if 'miRNA_sequencing' not in grouped_filters:
                    grouped_filters['miRNA_sequencing'] = []
                grouped_filters['miRNA_sequencing'].append({'filter': str(key), 'value': str(value)})
            elif key == 'has_UNC_HiSeq_RNASeq' or key == 'has_UNC_GA_RNASeq' or key == 'has_BCGSC_HiSeq_RNASeq' or key == 'has_BCGSC_GA_RNASeq':
                if 'RNA_sequencing' not in grouped_filters:
                    grouped_filters['RNA_sequencing'] = []
                grouped_filters['RNA_sequencing'].append({'filter': str(key), 'value': str(value)})
        # BQ-only format
        elif keyType == 'MUT':
            # If it's first in the list, don't append an "and"
            params = {}
            value_tuple += (params,)

            if first:
                first = False
            else:
                big_query_str += ' AND'

            big_query_str += " %s = '{hugo_symbol}' AND " % 'Hugo_Symbol'
            params['gene'] = gene

            if(key == 'category'):
                if value == 'any':
                    big_query_str += '%s IS NOT NULL' % 'Variant_Classification'
                    params['var_class'] = ''
                else:
                    big_query_str += '%s IN ({var_class})' % 'Variant_Classification'
                    values = MOLECULAR_CATEGORIES[value]
            else:
                big_query_str += '%s IN ({var_class})' % 'Variant_Classification'
                values = value

            if value != 'any':
                if isinstance(values, list):
                    j = 0
                    for vclass in values:
                        if j == 0:
                            params['var_class'] = "'%s'" % vclass.replace("'", "\\'")
                            j = 1
                        else:
                            params['var_class'] += ",'%s'" % vclass.replace("'", "\\'")
                else:
                    params['var_class'] = "'%s'" % values.replace("'", "\\'")

        else:
            # If it's first in the list, don't append an "and"
            if first:
                first = False
            else:
                query_str += ' and'
                big_query_str += ' and'

            # If it's age ranges, give it special treament due to normalizations
            if key == 'age_at_initial_pathologic_diagnosis':
                if value == 'None':
                    query_str += ' %s IS NULL' % key
                else:
                    query_str += ' (' + sql_age_by_ranges(value) + ') '
            # If it's age ranges, give it special treament due to normalizations
            elif key == 'BMI':
                if value == 'None':
                    query_str += ' %s IS NULL' % key
                else:
                    query_str += ' (' + sql_bmi_by_ranges(value) + ') '
            # If it's a list of items for this key, create an or subclause
            elif isinstance(value, list):
                has_null = False
                if 'None' in value:
                    has_null = True
                    query_str += ' (%s is null or' % key
                    big_query_str += ' (%s is null or' % key
                    value.remove('None')
                query_str += ' %s in (' % key
                big_query_str += ' %s in (' % key
                i = 0
                for val in value:
                    value_tuple += (val.strip(),) if type(val) is unicode else (val,)
                    if i == 0:
                        query_str += '%s'
                        big_query_str += '"' + str(val) + '"'
                        i += 1
                    else:
                        query_str += ',%s'
                        big_query_str += ',' + '"' + str(val) + '"'
                query_str += ')'
                big_query_str += ')'
                if has_null:
                    query_str += ')'
                    big_query_str += ')'

            # If it's looking for None values
            elif value == 'None':
                query_str += ' %s is null' % key
                big_query_str += ' %s is null' % key

            # For the general case
            else:
                if key == 'fl_archive_name':
                    big_query_str += ' %s like' % key
                    big_query_str += ' "%' + value + '%"'
                elif key == 'fl_data_level':
                    big_query_str += ' %s=%s' % (key, value)
                elif type(value) == bool:
                    big_query_str += ' %s=%r' % (key, value)
                else:
                    query_str += ' %s=' % key
                    big_query_str += ' %s=' % key
                    query_str += '%s'
                    big_query_str += '"%s"' % value
                    value_tuple += (value.strip(),) if type(value) is unicode else (value,)

    # Handle our data buckets
    if grouped_filters:
        for bucket in grouped_filters:
            if not query_str == '':
                query_str += ' and '
                big_query_str += ' and '

            query_str += '( '
            big_query_str += '( '

            first = True
            for filter in grouped_filters[bucket]:
                if first:
                    first = False
                else:
                    query_str += ' or '
                    big_query_str += ' or '

                query_str += ' %s=' % filter['filter']
                big_query_str += ' %s=' % filter['filter']
                query_str += '%s'
                big_query_str += '"%s"' % filter['value']
                value_tuple += (filter['value'].strip(),) if type(filter['value']) is unicode else (filter['value'],)

            query_str += ' )'
            big_query_str += ' )'

    return {'query_str': query_str, 'value_tuple': value_tuple, 'key_order': key_order, 'big_query_str': big_query_str}


def possible_future_authorization_function():
    # will put a decorator on this to ensure user has correct authorization before running
    # such as if they are dbgap authorized
    from oauth2client.client import flow_from_clientsecrets
    from oauth2client.file import Storage
    from oauth2client import tools
    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    flow = flow_from_clientsecrets(settings.CLIENT_SECRETS, scope='https://www.googleapis.com/auth/bigquery')
    ## in future, make storage file temporary somehow?
    storage = Storage('bigquery_credentials.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args([]))
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('bigquery', 'v2', http=http)
    return service


def authorize_credentials_with_Google():
    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    # documentation: https://developers.google.com/accounts/docs/application-default-credentials
    SCOPES = ['https://www.googleapis.com/auth/bigquery']
    # credentials = GoogleCredentials.get_application_default().create_scoped(SCOPES)
    credentials = GoogleCredentials.from_stream(settings.GOOGLE_APPLICATION_CREDENTIALS).create_scoped(SCOPES)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('bigquery', 'v2', http=http)
    if debug: print >> sys.stderr,' big query authorization '+sys._getframe().f_code.co_name
    return service

# TODO refactor to remove duplicate code
def authorize_credentials_with_google_from_file(credentials_path):
    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    # documentation: https://developers.google.com/accounts/docs/application-default-credentials
    SCOPES = ['https://www.googleapis.com/auth/bigquery']
    credentials = GoogleCredentials.from_stream(credentials_path).create_scoped(SCOPES)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('bigquery', 'v2', http=http)

    return service


def get_user_email_from_token(access_token):
    if debug: print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
    user_email = None
    credentials = AccessTokenCredentials(access_token, 'test-user')
    http = credentials.authorize(httplib2.Http())
    user_info_service = build('oauth2', 'v2', http=http)
    user_info = user_info_service.userinfo().get().execute()
    if 'email' in user_info:
        user_email = user_info['email']
    return user_email
