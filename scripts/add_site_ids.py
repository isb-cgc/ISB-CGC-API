#
# Copyright 2015-2024, Institute for Systems Biology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import print_function

import os
import MySQLdb
import logging
import traceback
import sys
from django.conf import settings

logging.basicConfig(level=logging.INFO)

db = None
cursor = None

try:

    db_settings = settings.DATABASES.get('default')
    if not settings.CONNECTION_IS_LOCAL:
        raise Exception("This script should never be run on a deployed system!")
    ssl = db_settings.get('OPTIONS', {}).get('ssl', None)
    db = MySQLdb.connect(host=db_settings['HOST'], db=db_settings['NAME'], user=db_settings['USER'], passwd=db_settings['PASSWORD'], ssl=ssl)

    delete_str = 'DELETE FROM django_site WHERE id in (2, 3, 4, 5);'
    insert_str = 'INSERT INTO django_site (id, domain, name) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s);'

    insert_tuple = ('2', 'localhost:8000', 'localhost:8000')
    insert_tuple += ('3', 'localhost:8080', 'localhost:8080')
    insert_tuple += ('4', 'dev.isb-cgc.org', 'dev.isb-cgc.org')

    cursor = db.cursor()
    cursor.execute(delete_str)
    cursor.execute(insert_str, insert_tuple)
    db.commit()

except Exception as e:
    print("[ERROR] Exception in add_site_ids: ", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
finally:
    if cursor: cursor.close()
    if db and db.open: db.close()
