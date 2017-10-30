'''
copyright 2017, Institute for Systems Biology.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from argparse import ArgumentParser
from datetime import datetime
import MySQLdb

def get_sql_connection(args):
    try:
        connect_options = {
            'host': args.host,
            'db': args.database,
            'user': args.user,
            'passwd': args.password,
            'ssl': {
                'ca': args.ssl_ca,
                'key': args.ssl_key,
                'cert': args.ssl_cert
            }
        }
        db = MySQLdb.connect(**connect_options)
    except:
        print 'failed'
        raise
    return db

FIELD_TYPES ={
    'varchar': 'StringField',
    'float': 'FloatField',
    'tinyint': 'BooleanField',
    'int': 'IntegerField'
}

seen_rows = set()
def write_allowed_values(cursor, rows, path, program, metadata_type, column_filter, append_file=True, complete_file=False, write_file=False):
    if not write_file:
        return

    MAX_VALUES = 70
    try:
        mode = 'a+' if append_file else 'w'
        with open(path, mode) as av:
            if not append_file:
                av.write('{\n')
            av.write('    "{}": {{\n'.format(metadata_type))
            table_name = 'Clinical' if 'Common' == metadata_type else metadata_type
            query = 'select {} from %s_metadata_%s group by 1 order by 1' % (program, table_name[:1].lower() + table_name[1:])
            body = ''
            for row in rows:
#                 if row['DATA_TYPE'] != 'varchar' or row['COLUMN_NAME'] in seen_rows:
                if row['DATA_TYPE'] != 'varchar':
                    continue
                if ('Common' in metadata_type and row['COLUMN_NAME'] not in column_filter) or ('Common' not in metadata_type and row['COLUMN_NAME'] in column_filter):
                    continue
                
                seen_rows.add(row['COLUMN_NAME'])
                cursor.execute(query.format(row['COLUMN_NAME']))
                currows = cursor.fetchall()
                if MAX_VALUES < len(currows):
                    continue
                if 1 == len(currows) and 'None' == currows[0][row['COLUMN_NAME']]:
                    continue
                
                body += '        "{}": [\n            {}\n        ],\n'.format(row['COLUMN_NAME'], '            '.join('"{}",\n'.format(currow[row['COLUMN_NAME']]) for currow in currows if not currow[row['COLUMN_NAME']] is None)[:-2])
            av.write(body[:-2])
            av.write('\n    }')
                
            if complete_file:
                av.write('\n}\n')
            else:
                av.write(',\n')
            av.flush()
            return
    except:
        cursor.close()
        raise
        
def create_nesting_class(table_list, path, write_file):
    if not write_file:
        return

    with open(path, 'a') as f:
        ranges_body = 'class MetadataRangesItem(messages.Message):\n'
        items_body = 'class MetadataItem(messages.Message):\n'
        for index, table in enumerate(table_list):
            ranges_body += '    {0} = messages.MessageField({0}MetadataRangesItem, {1})\n'.format(table, index+1)
            items_body += '    {0} = messages.MessageField({0}MetadataItem, {1})\n'.format(table, index+1)
        f.write('{}\n'.format(ranges_body))
        f.write('{}\n'.format(items_body))

def write_metadata_file(class_name, rows, path, append_file=True, write_file=False):

    ranges_text = 'class {}RangesItem(messages.Message):\n    '.format(class_name)
    
    i = 1
    for row in rows:
        field_type = FIELD_TYPES.get(row['DATA_TYPE'])
        if not field_type:
            continue
        ranges_text += '%-65s = messages.%s(%d, repeated=True' % (row['COLUMN_NAME'], field_type, i)
        ranges_text += ')\n    ' if field_type is not 'IntegerField' else ', variant=messages.Variant.INT32)\n    '
        i += 1

        if field_type == 'IntegerField' or field_type == 'FloatField':
            ranges_text += '%-65s = messages.%s(%d' % (row['COLUMN_NAME']+'_lte', field_type, i)
            ranges_text += ')\n    ' if field_type is not 'IntegerField' else ', variant=messages.Variant.INT32)\n    '
            i += 1
            ranges_text += '%-65s = messages.%s(%d' % (row['COLUMN_NAME']+'_gte', field_type, i)
            ranges_text += ')\n    ' if field_type is not 'IntegerField' else ', variant=messages.Variant.INT32)\n    '
            i += 1
            ranges_text += '\n    '

    item_text = '\nclass {}Item(messages.Message):\n    '.format(class_name)
    i = 1
    for row in rows:
        field_type = FIELD_TYPES.get(row['DATA_TYPE'])
        if not field_type:
            continue
        item_text += '%-65s = messages.%s(%d' % (row['COLUMN_NAME'], field_type, i)
        item_text += ')\n    ' if field_type is not 'IntegerField' else ', variant=messages.Variant.INT32)\n    '
        i += 1
    
    if write_file is True:
        mode = 'a' if append_file else 'w'
        with open(path, mode) as f:
            if not append_file:
                f.write('from protorpc import messages\n\n')
            f.write(ranges_text)
            f.write(item_text + '\n')
    else:
        print path + '\n'
        print ranges_text
        print '\n\n'
        print item_text

def get_table_column_info(cursor, program, metadata_type, column_filter = []):
    key_part = metadata_type.split('_')[0].lower()
    table_name = 'Clinical' if 'Common' == metadata_type else metadata_type
    query_str = 'SELECT COLUMN_NAME, DATA_TYPE, COLUMN_TYPE ' \
                'FROM INFORMATION_SCHEMA.COLUMNS ' \
                'WHERE table_name = "{}_metadata_{}" ' \
                        'AND COLUMN_NAME != "metadata_{}_id" ' + 'group by COLUMN_NAME, DATA_TYPE, COLUMN_TYPE ' \
                         'ORDER BY column_name'
    cursor.execute(query_str.format(program, table_name[:1].lower() + table_name[1:], key_part))
    rows = cursor.fetchall()
    retrows = []
    seen = set()
    for row in rows:
        if ('Common' in metadata_type and row['COLUMN_NAME'] not in column_filter) or ('Common' not in metadata_type and row['COLUMN_NAME'] in column_filter):
            continue
        if row['COLUMN_NAME'] in seen:
            continue
        seen.add(row['COLUMN_NAME'])
        retrows += [row]
    return retrows

def create_metadata_file(cursor, program, metadata_type, path, column_filter, append_file=True, complete_file=False, write_file=True):
    rows = get_table_column_info(cursor, program, metadata_type, column_filter)
    write_metadata_file(metadata_type + 'Metadata', rows, path, append_file, write_file)
    path = 'api_3/isb_cgc_api_{0}/allowed_values_v3_{0}.json'.format(program)
    write_allowed_values(cursor, rows, path, program, metadata_type, column_filter, append_file, complete_file, write_file)
    return rows

def main(args):
    db = get_sql_connection(args)
    cursor = None
    try:
        path_template = 'api_3/isb_cgc_api_%s/message_classes.py'
        programs = [
            ('CCLE', False),
            ('TARGET', False),
            ('TCGA', True),
        ]
        for program in programs:
            print datetime.now(), 'starting program {}'.format(program)
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
            write_file = not bool(args.dry_run)
            # for the columns that are common to all tables and have the same values from the subsequent tables, get them here and any filters
            column_filter = ["disease_code", "endpoint_type", "program_name", "project_short_name"]
            create_metadata_file(cursor, program[0], 'Common', path_template % (program[0]), column_filter, False, False, write_file)
            column_filter += [
                'acl',
                'analysis_gdc_id',
                'analysis_workflow_link',
                'archive_gdc_id',
                'archive_revision',
                'archive_revision_lte',
                'archive_revision_gte',
                'file_gdc_id',
                'file_name_key',
                'index_file_id',
                'md5sum',
                'type'
            ]
            create_metadata_file(cursor, program[0], 'Clinical', path_template % (program[0]), column_filter, True, False, write_file)
            column_filter += ["disease_code", "endpoint_type", "program_name", "project_short_name"]
            create_metadata_file(cursor, program[0], 'Biospecimen', path_template % (program[0]), column_filter, True, False, write_file)
            table_list = ['Common', 'Clinical', 'Biospecimen', 'Data_HG19']
            create_metadata_file(cursor, program[0], 'Data_HG19', path_template % (program[0]), column_filter, True, True if 'CCLE' == program[0] else False, write_file)
            if 'CCLE' != program[0]:
                create_metadata_file(cursor, program[0], 'Data_HG38', path_template % (program[0]), column_filter, True, False if program[1] else True, write_file)
                table_list += ['Data_HG38']
            create_nesting_class(table_list, path_template % (program[0]), write_file)
            if program[1]:
                create_metadata_file(cursor, program[0], 'Annotation', path_template % (program[0]), column_filter, True, True, write_file)
            print datetime.now(), 'finished program {}'.format(program)
    finally:
        if cursor:
            cursor.close()
        db.close()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host', help='database host')
    parser.add_argument('--database', '-d', help='database name')
    parser.add_argument('--user', '-u', help='database username')
    parser.add_argument('--password', '-p', help='database password')
    parser.add_argument('--ssl_key')
    parser.add_argument('--ssl_cert')
    parser.add_argument('--ssl_ca')
    parser.add_argument('--dry_run', dest='dry_run', action='store_true')
    parser.add_argument('--write_file', dest='dry_run', action='store_false')
    parser.set_defaults(feature=True)
    args = parser.parse_args()

    print datetime.now(), 'starting...'
    main(args)
    print datetime.now(), 'finished'


