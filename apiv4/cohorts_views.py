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

logger = logging.getLogger(__name__)


def convert_api_filters(filter_obj, by_prog=False, prog_by_attr=False, attr_to_id=False):
    pass

# Requires login
def get_file_manifest(cohort_id, user):
    pass


# Requires login
def get_cohort_info(cohort_id, user, get_barcodes=False):
    pass

# Preview method for a cohort, or to get a cohort's case listing; does not require login as it is filter-based
def get_cohort_counts():
    pass


# Requires login
def create_cohort(user):
    pass


# Requires login
def edit_cohort(cohort_id, user, delete=False):
    pass