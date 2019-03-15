import os
import sys
from google.appengine.ext import vendor
import logging

logger = logging.getLogger(__name__)

print("In appengine_config.py")

# Add any libraries installed in the "lib" folder.
vendor.add('lib')

SHARED_SOURCE_DIRECTORIES = [
    os.path.abspath('./ISB-CGC-Common'),
    os.path.abspath('./google_appengine')
]

# Add the shared Django application subdirectory to the Python module search path
for path in SHARED_SOURCE_DIRECTORIES:
    sys.path.append(path)

import django
django.setup()
