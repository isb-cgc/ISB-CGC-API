# 
# Copyright 2019, Institute for Systems Biology
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

import logging
import json
import django

from flask import request

from django.conf import settings

from projects.models import Program, Project
from accounts.models import AuthorizedDataset

logger = logging.getLogger(settings.LOGGER_NAME)


def get_cohort_programs():
    django.setup()
    program_info = None
    try:
        program_info = [
            {
                'name': x.name,
                'description': x.description,
                'projects': [{'name': y.name, 'description': y.description} for y in Project.objects.filter(program=x,active=1)]
            }
            for x in Program.get_public_programs()
        ]
    except Exception as e:
        logger.exception(e)

    return program_info


def get_dataset_for_reg():
    django.setup()
    datasets = None
    try:
        datasets = [
            {
                'name': x.name,
                'dataset_id': x.whitelist_id
            }
            for x in AuthorizedDataset.get_public_datasets()
        ]
    except Exception as e:
        logger.exception(e)

    return datasets
