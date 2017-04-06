"""

Copyright 2017, Institute for Systems Biology

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
import endpoints
from django.conf import settings

INSTALLED_APP_CLIENT_ID = settings.INSTALLED_APP_CLIENT_ID

ISB_CGC_TCGA_Endpoints = endpoints.api(name='isb_cgc_tcga_api', version='v3',
                                  description="Get information about cohorts, cases, and samples for TCGA. Create and delete cohorts.",
                                  allowed_client_ids=[INSTALLED_APP_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID,
                                                      settings.WEB_CLIENT_ID],
                                  documentation='http://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/Programmatic-API.html#isb-cgc-api-v3',
                                  title="ISB-CGC TCGA API")
