#!/usr/bin/env bash

source ../venv/bin/activate
#pip install openapi2jsonschema
echo $PWD
# Convert the Swagger yaml file to JSON schema format
openapi2jsonschema ../openapi-appengine.yaml --stand-alone -o ../api/schemas

# Convert the filterset schema into a python file that can be imported
sed '1s/.*/COHORT_FILTER_SCHEMA\=&/' ../api/schemas/filterset.json > ../api/schemas/filterset.py
rm ../api/schemas/*.json