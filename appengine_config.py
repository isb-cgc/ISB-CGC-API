import os
import sys
from google.appengine.ext import vendor

import logging

logger = logging.getLogger(__name__)

# Add any libraries installed in the "lib" folder.
vendor.add('lib')

BASE_DIR                = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + os.sep

SHARED_SOURCE_DIRECTORIES = [
   os.path.abspath('./ISB-CGC-Common')
]

# Add the shared Django application subdirectory to the Python module search path
for path in SHARED_SOURCE_DIRECTORIES:
    sys.path.append(path)

logger.info("Checking dir listing in appengine_config:")
logger.info(os.listdir())
import django
django.setup()
