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
    'int': 'IntegerField',
    'datetime': 'datetime'
}

def write_allowed_values(db, rows, path, program, write_file=False):
# 'DATA_TYPE': 'int', 'COLUMN_NAME': 'age_began_smoking_in_years'
    if not write_file:
        return

    MAX_VALUES = 70
    cursor = db.cursor()
    seen_rows = set()
    try:
        with open(path, 'w') as av:
            av.write('{\n')
            clinical_query = 'select {} from %s_metadata_clinical group by 1 order by 1' % (program)
            biospecimen_query = 'select {} from %s_metadata_biospecimen group by 1 order by 1' % (program)
            body = ''
            for row in rows:
                if row['DATA_TYPE'] != 'varchar' or row['COLUMN_NAME'] in seen_rows:
                    continue
                seen_rows.add(row['COLUMN_NAME'])
                try:
                    currows = get_table_column_info(cursor, clinical_query.format(row['COLUMN_NAME']))
                except:
                    currows = get_table_column_info(cursor, biospecimen_query.format(row['COLUMN_NAME']))
                if MAX_VALUES < len(currows):
                    continue
                
                body += '    "{}": [\n        {}\n    ],\n'.format(row['COLUMN_NAME'], '        '.join('"{}",\n'.format(value[0]) for value in currows)[:-2])
            av.write(body[:-2])
            av.write('\n}\n')
             
    except:
        cursor.close()
        

def write_metadata_file(rows, path, write_file=False):

    ranges_text = 'class MetadataRangesItem(messages.Message):\n    '
    
    seen_rows = set()
    shared_rows = []
    i = 1
    for row in rows:
        if row['COLUMN_NAME'] in seen_rows:
            shared_rows += [row['COLUMN_NAME']]
            continue
        
        seen_rows.add(row['COLUMN_NAME'])
        field_type = FIELD_TYPES.get(row['DATA_TYPE'])
#         if field_type == 'IntegerField' or field_type == 'FloatField' and i > 1:
#             ranges_text += '\n    '

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

    item_text = '\nclass MetadataItem(messages.Message):\n    '
    seen_rows = set()
    i = 1
    for row in rows:
        if row['COLUMN_NAME'] in seen_rows:
            continue
            
        seen_rows.add(row['COLUMN_NAME'])
        field_type = FIELD_TYPES.get(row['DATA_TYPE'])
        item_text += '%-65s = messages.%s(%d' % (row['COLUMN_NAME'], field_type, i)
        item_text += ')\n    ' if field_type is not 'IntegerField' else ', variant=messages.Variant.INT32)\n    '
        i += 1
    
    shared_text = '\nshared_fields = [%s]\n' % (', '.join("'" + row + "'" for row in shared_rows))
    
    if write_file is True:
        with open(path, 'w') as f:
            f.write('from protorpc import messages\n\n')
            f.write(ranges_text)
            f.write(item_text)
            f.write(shared_text)
    else:
        print path + '\n'
        print ranges_text
        print '\n\n'
        print item_text
        print '\n\n'
        print shared_text


def write_annotation_file(rows, path, write_file=False):
    item_text = '\nclass MetadataAnnotationItem(messages.Message):\n    '
    i = 1
    for row in rows:
        field_type = FIELD_TYPES.get(row['DATA_TYPE'])
        if field_type.lower() == 'datetime': continue
        item_text += '%-30s = messages.%s(%d' % (row['COLUMN_NAME'], field_type, i)
        item_text += ')\n    ' if field_type is not 'IntegerField' else ', variant=messages.Variant.INT32)\n    '
        i += 1

    if write_file is True:
        with open(path, 'a') as f:
            f.write('\n')
            f.write(item_text)
    else:
        print item_text


def get_table_column_info(cursor, query_str):
    cursor.execute(query_str)
    rows = cursor.fetchall()
    return rows

def main(args):
    db = get_sql_connection(args)
    cursor = None
    try:
        path_template = 'api_3/isb_cgc_api_%s/message_classes.py'
        programs = [
            ('TCGA', True),
            ('TARGET', False),
            ('CCLE', False),
        ]
        for program in programs:
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            query_str = 'SELECT COLUMN_NAME, DATA_TYPE, COLUMN_TYPE ' \
                        'FROM INFORMATION_SCHEMA.COLUMNS '
            clinical_query_str = query_str + 'WHERE table_name = "%s_metadata_clinical" ' \
                        'AND COLUMN_NAME != "metadata_clinical_id" ' + 'group by COLUMN_NAME, DATA_TYPE, COLUMN_TYPE ' \
                         'ORDER BY column_name'
        
            biospecimen_query_str = query_str + 'WHERE table_name = "%s_metadata_biospecimen" ' \
                        'AND COLUMN_NAME != "metadata_biospecimen_id" ' + 'group by COLUMN_NAME, DATA_TYPE, COLUMN_TYPE ' \
                         'ORDER BY column_name'
        
            write_file = not bool(args.dry_run)
        
            combined_rows = []
            for cur_query_str in [clinical_query_str, biospecimen_query_str]:
                combined_rows += list(get_table_column_info(cursor, cur_query_str % (program[0])))
            write_metadata_file(combined_rows, path_template % (program[0]), write_file=write_file)
        
            if program[1]:
                annotation_query_str = query_str + 'WHERE table_name = "%s_metadata_annotation" ' \
                            'AND COLUMN_NAME != "metadata_annotation_id" ' + 'group by COLUMN_NAME, DATA_TYPE, COLUMN_TYPE ' \
                             'ORDER BY column_name'
                write_annotation_file(get_table_column_info(cursor, annotation_query_str % (program[0])), path_template % (program[0]), write_file=write_file)
            
            path = 'api_3/isb_cgc_api_{0}/allowed_values_v3_{0}.json'.format(program[0])
            write_allowed_values(db, combined_rows, path, program[0], write_file)
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

    main(args)


