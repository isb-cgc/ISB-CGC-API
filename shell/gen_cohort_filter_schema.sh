#!/usr/bin/env bash

source ../venv/bin/activate
#pip install openapi2jsonschema
echo $PWD
# Convert the Swagger yaml file to JSON schema format
openapi2jsonschema ../openapi-appengine.yaml --stand-alone -o ../api/schemas

# Convert the filterset schema into a python file that can be imported
sed '1s/.*/COHORT_FILTER_SCHEMA\=&/' ../api/schemas/filterset.json > ../api/schemas/filterset.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/schemas/filterset.py

# Convert the filterset schema into a python file that can be imported
sed '1s/.*/QUERY_PREVIEW_BODY\=&/' ../api/schemas/querypreviewbody.json > ../api/schemas/querypreviewbody.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/schemas/querypreviewbody.py

# Convert the filterset schema into a python file that can be imported
sed '1s/.*/QUERY_FIELDS\=&/' ../api/schemas/queryfields.json > ../api/schemas/queryfields.py
sed "-i" "" "-e" 's/"additionalProperties": false/"additionalProperties": False/' ../api/schemas/queryfields.py


rm ../api/schemas/*.json