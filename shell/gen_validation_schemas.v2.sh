#!/usr/bin/env bash

# Generate JSON encoded components of the openapi_appengine.v2.yaml that will be
# used to validate parameterization

set -x
source ../venv/bin/activate
#pip install openapi2jsonschema
echo $PWD
# Convert the v2 Swagger yaml file to JSON schema format
openapi2jsonschema ../api/v2/tools/filters.yaml --stand-alone -o ../api/v2/schemas
# Convert the filters schema into a python file that can be imported
sed '1s/.*/COHORT_FILTERS_SCHEMA\=&/' ../api/v2/schemas/filters.json > ../api/v2/schemas/filters.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/v2/schemas/filters.py

openapi2jsonschema ../api/v2/tools/fields.yaml --stand-alone -o ../api/v2/schemas
# Convert the filterset schema into a python file that can be imported
sed '1s/.*/FIELDS\=&/' ../api/v2/schemas/fields.json > ../api/v2/schemas/fields.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/v2/schemas/fields.py


rm ../api/v2/schemas/*.json