#!/bin/bash

#set -x

DATE=$(date '+%Y%m%d_%H%M%S')

# Save the current version with a datetime stamp

cp openapi-appengine.yaml dev.openapi-appengine.yaml
sed -i "" 's/#host: "dev-api.canceridc.dev"/host: "dev-api.canceridc.dev"/' dev.openapi-appengine.yaml
sed -i "" 's/#- "https"/- "https"/' dev.openapi-appengine.yaml
sed -i "" 's/- "http"/#- "http"/' dev.openapi-appengine.yaml

cp openapi-appengine.yaml test.openapi-appengine.yaml
sed -i "" 's/#host: "testing-api.canceridc.dev"/host: "testing-api.canceridc.dev"/' test.openapi-appengine.yaml
sed -i "" 's/x-google-audiences: "94/#x-google-audiences: "94/'  test.openapi-appengine.yaml
sed -i "" 's/#x-google-audiences: "10/x-google-audiences: "10/'  test.openapi-appengine.yaml
sed -i "" 's/#- "https"/- "https"/' test.openapi-appengine.yaml
sed -i "" 's/- "http"/#- "http"/' test.openapi-appengine.yaml
PWD
gcloud auth login bcliffor@systemsbiology.org
gsutil cp openapi-appengine.yaml gs://idc-api-dev-files/openapi-api.yaml.${DATE}

gsutil cp dev.openapi-appengine.yaml gs://idc-deployment-files/dev/dev.openapi-appengine.yaml

gcloud auth login bcliffor@canceridc.dev
gsutil cp test.openapi-appengine.yaml gs://webapp-deployment-files-idc-test/test.openapi-appengine.yaml
gcloud auth login bcliffor@systemsbiology.org