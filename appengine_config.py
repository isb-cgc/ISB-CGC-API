import os
import sys
from google.appengine.ext import vendor

# Per https://github.com/GoogleCloudPlatform/google-cloud-python/issues/1705#issuecomment-209721632 we have to unload
# some GAE-installed libs to make sure our newer versions are used
def unload_module(module_name):
    target_modules = [m for m in sys.modules if m.startswith(module_name)]
    for m in target_modules:
        if m in sys.modules:
            del sys.modules[m]

# Add any libraries installed in the "lib" folder.
vendor.add('lib')

# The default endpoints/GAE oauth2 is way too old.
unload_module('oauth2client')

import oauth2client
print >> sys.stdout, "OAuth2 is now:" + str(oauth2client.__version__)

BASE_DIR                = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + os.sep

SHARED_SOURCE_DIRECTORIES = [
   os.path.abspath('./ISB-CGC-Common')
]

# Add the shared Django application subdirectory to the Python module search path
for path in SHARED_SOURCE_DIRECTORIES:
    sys.path.append(path)

# Initialize Django (when running ISB-CGC-API as standalone using dev_appserver.py)
import django
django.setup()
