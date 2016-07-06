
from argparse import ArgumentParser
import MySQLdb

def get_sql_connection(args):
    try:
        connect_options = {
            'host': args.host,
            'db': args.name,
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

def write_file(rows):

    ranges_text = 'class MetadataRangesItem(messages.Message):\n    '
    i = 1
    for row in rows:
        field_type = FIELD_TYPES.get(row['DATA_TYPE'])
        if field_type == 'IntegerField' or field_type == 'FloatField' and i > 1:
            ranges_text += '\n    '

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
    i = 1
    for row in rows:
        field_type = FIELD_TYPES.get(row['DATA_TYPE'])
        item_text += '%-65s = messages.%s(%d' % (row['COLUMN_NAME'], field_type, i)
        item_text += ')\n    ' if field_type is not 'IntegerField' else ', variant=messages.Variant.INT32)\n    '
        i += 1

    with open('message_classes.py', 'w') as f:
        f.write('from protorpc import messages\n\n\n')
        f.write(ranges_text)
        f.write(item_text)


def main(args):
    db = get_sql_connection(args)
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    query_str = '''
    SELECT COLUMN_NAME, DATA_TYPE, COLUMN_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE table_name = 'metadata_samples'
    AND COLUMN_NAME != 'metadata_samples_id'
    ORDER BY column_name
    '''
    cursor.execute(query_str)
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    write_file(rows)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host', help='database host')
    parser.add_argument('--name', '-n', help='database name')
    parser.add_argument('--user', '-u', help='database username')
    parser.add_argument('--password', '-p', help='database password')
    parser.add_argument('--ssl_key')
    parser.add_argument('--ssl_cert')
    parser.add_argument('--ssl_ca')
    args = parser.parse_args()

    main(args)