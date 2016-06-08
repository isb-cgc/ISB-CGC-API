import os
import sys

from google.appengine.ext import vendor
# Add any libraries installed in the "lib" folder.
vendor.add('lib')

BASE_DIR                = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + os.sep

SHARED_SOURCE_DIRECTORIES = [
   os.path.abspath(os.environ.get('ISB_CGC_COMMON_MODULE_PATH'))
]

# Add the shared Django application subdirectory to the Python module search path
for path in SHARED_SOURCE_DIRECTORIES:
    sys.path.append(path)
