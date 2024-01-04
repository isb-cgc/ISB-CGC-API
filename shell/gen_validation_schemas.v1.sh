#!/usr/bin/env bash

# Generate JSON schemas that are used to validate parameterization

set -x
source ../venv/bin/activate
#pip install openapi2jsonschema
echo $PWD
# Convert the v1 Swagger yaml file to JSON schema format
openapi2jsonschema ../api/v1/tools/filters.yaml --stand-alone -o ../api/v1/schemas

# Convert the filterset schema into a python file that can be imported
sed '1s/.*/COHORT_FILTERS_SCHEMA\=&/' ../api/v1/schemas/filters.json > ../api/v1/schemas/filters.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/v1/schemas/filters.py

openapi2jsonschema ../api/v1/tools/queryfields.yaml --stand-alone -o ../api/v1/schemas
# Convert the filterset schema into a python file that can be imported
sed '1s/.*/QUERY_FIELDS\=&/' ../api/v1/schemas/queryfields.json > ../api/v1/schemas/queryfields.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/v1/schemas/queryfields.py


rm ../api/v1/schemas/*.json