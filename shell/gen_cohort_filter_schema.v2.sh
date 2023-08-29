#!/usr/bin/env bash
set -x
source ../venv/bin/activate
#pip install openapi2jsonschema
echo $PWD
# Convert the v2 Swagger yaml file to JSON schema format
openapi2jsonschema ../api/v2/tools/filters.yaml --stand-alone -o ../api/v2/schemas

# Convert the filterset schema into a python file that can be imported
sed '1s/.*/COHORT_FILTERS_SCHEMA\=&/' ../api/v2/schemas/filters.json > ../api/v2/schemas/filters.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/v2/schemas/filters.py

openapi2jsonschema ../api/v2/tools/queryfields.yaml --stand-alone -o ../api/v2/schemas
# Convert the filterset schema into a python file that can be imported
sed '1s/.*/QUERY_FIELDS\=&/' ../api/v2/schemas/queryfields.json > ../api/v2/schemas/queryfields.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/v2/schemas/queryfields.py


rm ../api/v2/schemas/*.json