#!/bin/bash

#set -x

DATE=$(date '+%Y%m%d_%H%M%S')

# Save the current version with a datetime stamp
gcloud auth login bcliffor@systemsbiology.org
gsutil cp openapi-appengine.v1.yaml gs://idc-api-dev-files/openapi-api.v1.yaml.${DATE}
gsutil cp openapi-appengine.v2.yaml gs://idc-api-dev-files/openapi-api.v2.yaml.${DATE}
