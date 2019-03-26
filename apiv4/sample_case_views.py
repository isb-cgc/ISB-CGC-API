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

from django.conf import settings
from cohorts.metadata_helpers import get_sample_case_metadata

logger = logging.getLogger(settings.LOGGER_NAME)


def get_full_sample_metadata(sample_barcode):
    metadata = get_sample_case_metadata([sample_barcode], False)

    if len(metadata.keys()):
        return metadata
    else:
        return None


def get_case_metadata(case_barcode):
    metadata = get_sample_case_metadata([case_barcode], True)

    if len(metadata.keys()):
        return metadata
    else:
        return None
