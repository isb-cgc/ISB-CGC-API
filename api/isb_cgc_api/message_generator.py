
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
    print rows
    cursor.close()
    db.close()

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