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

logger = logging.getLogger(__name__)


def get_cohort_programs():
    django.setup()
    program_info = None
    try:
        name = request.args.get('name', default='%', type=str) if 'name' in request.args else None
        desc = request.args.get('desc', default='%', type=str) if 'desc' in request.args else None

        results = Program.get_public_programs(name=name, desc=desc)

        program_info = [
            {
                'name': x.name,
                'description': x.description,
                'program_privacy': "Public",
                'projects': [{'name': y.name, 'description': y.description} for y in x.project_set.all()]
            }
            for x in results
        ]
    except Exception as e:
        logger.exception(e)

    return program_info
