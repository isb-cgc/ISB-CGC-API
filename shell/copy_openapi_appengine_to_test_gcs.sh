#!/bin/bash

#set -x

DATE=$(date '+%Y%m%d_%H%M%S')

cp openapi-appengine.v1.yaml test.openapi-appengine.v1.yaml
sed -i "" 's/#host: "testing-api.canceridc.dev"/host: "testing-api.canceridc.dev"/' test.openapi-appengine.v1.yaml
sed -i "" 's/x-google-audiences: "94/#x-google-audiences: "94/'  test.openapi-appengine.v1.yaml
sed -i "" 's/#x-google-audiences: "10/x-google-audiences: "10/'  test.openapi-appengine.v1.yaml
sed -i "" 's/#- "https"/- "https"/' test.openapi-appengine.v1.yaml
sed -i "" 's/- "http"/#- "http"/' test.openapi-appengine.v1.yaml
cp openapi-appengine.v2.yaml test.openapi-appengine.v2.yaml
sed -i "" 's/#host: "testing-api.canceridc.dev"/host: "testing-api.canceridc.dev"/' test.openapi-appengine.v2.yaml
sed -i "" 's/x-google-audiences: "94/#x-google-audiences: "94/'  test.openapi-appengine.v2.yaml
sed -i "" 's/#x-google-audiences: "10/x-google-audiences: "10/'  test.openapi-appengine.v2.yaml
sed -i "" 's/#- "https"/- "https"/' test.openapi-appengine.v2.yaml
sed -i "" 's/- "http"/#- "http"/' test.openapi-appengine.v2.yaml

gcloud auth login bcliffor@canceridc.dev
gsutil cp test.openapi-appengine.v1.yaml gs://webapp-deployment-files-idc-test/test.openapi-appengine.v1.yaml
gsutil cp test.openapi-appengine.v2.yaml gs://webapp-deployment-files-idc-test/test.openapi-appengine.v2.yaml
gcloud auth login bcliffor@systemsbiology.org