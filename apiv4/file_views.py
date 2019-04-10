"""

Copyright 2019, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import logging
import json
import django

from flask import request

from django.core.signals import request_finished
from django.conf import settings
from cohorts.metadata_helpers import get_paths_by_uuid

from auth import UserValidationException

logger = logging.getLogger(settings.LOGGER_NAME)


def get_file_paths(file_uuids):
    if not file_uuids or not len(file_uuids):
        raise Exception("While attempting to obtain file paths, encountered an error: no file UUIDs were provided.")

    paths = get_paths_by_uuid(file_uuids)

    return paths


def get_signed_uris(user, file_uuids):
    if not user:
        logger.error("A user was not provided while attempting to obtained signed URIs!")
        raise UserValidationException("A user was not provided while attempting to obtained signed URIs!")
    if not file_uuids or not len(file_uuids):
        raise Exception("While attempting to obtain signed URIs, encountered an error: no file UUIDs were provided.")
    
    return []




