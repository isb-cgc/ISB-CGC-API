import sys
import MySQLdb

from protorpc import messages
from api.api_helpers import sql_connection


def main(table_name):
    fields = []
    try:
        db = sql_connection()
        cursor = db.cursor()
        cursor.execute("describe {}".format(table_name))

        for row in cursor.fetchall():
            if row['field'] == 'metadata_samples_id':
                continue
            fields.append((row['field'], row['type'],))
    except (IndexError, TypeError, MySQLdb.ProgrammingError) as e:
        db.close()
        print e
    finally:
        db.close()
    fields = sorted(fields, key=lambda x: x[0].lower())
    print fields






if __name__ == '__main__':
    table_name = sys.argv[1]
    main(table_name)