#!/bin/bash

#set -x

DATE=$(date '+%Y%m%d_%H%M%S')

# Save the current version with a datetime stamp

cp openapi-appengine.v1.yaml dev.openapi-appengine.v1.yaml
sed -i "" 's/#host: "dev-api.canceridc.dev"/host: "dev-api.canceridc.dev"/' dev.openapi-appengine.v1.yaml
sed -i "" 's/#- "https"/- "https"/' dev.openapi-appengine.v1.yaml
sed -i "" 's/- "http"/#- "http"/' dev.openapi-appengine.v1.yaml
cp openapi-appengine.v2.yaml dev.openapi-appengine.v2.yaml
sed -i "" 's/#host: "dev-api.canceridc.dev"/host: "dev-api.canceridc.dev"/' dev.openapi-appengine.v2.yaml
sed -i "" 's/#- "https"/- "https"/' dev.openapi-appengine.v2.yaml
sed -i "" 's/- "http"/#- "http"/' dev.openapi-appengine.v2.yaml

gcloud auth login bcliffor@systemsbiology.org
gsutil cp openapi-appengine.v1.yaml gs://idc-api-dev-files/openapi-api.v1.yaml.${DATE}
gsutil cp dev.openapi-appengine.v1.yaml gs://idc-deployment-files/dev/dev.openapi-appengine.v1.yaml
gsutil cp openapi-appengine.v2.yaml gs://idc-api-dev-files/openapi-api.v2.yaml.${DATE}
gsutil cp dev.openapi-appengine.v2.yaml gs://idc-deployment-files/dev/dev.openapi-appengine.v2.yaml
