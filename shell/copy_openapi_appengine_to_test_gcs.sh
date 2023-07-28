#!/bin/bash

#set -x

DATE=$(date '+%Y%m%d_%H%M%S')

cp openapi-appengine.yaml test.openapi-appengine.yaml
sed -i "" 's/#host: "testing-api.canceridc.dev"/host: "testing-api.canceridc.dev"/' test.openapi-appengine.yaml
sed -i "" 's/x-google-audiences: "94/#x-google-audiences: "94/'  test.openapi-appengine.yaml
sed -i "" 's/#x-google-audiences: "10/x-google-audiences: "10/'  test.openapi-appengine.yaml
sed -i "" 's/#- "https"/- "https"/' test.openapi-appengine.yaml
sed -i "" 's/- "http"/#- "http"/' test.openapi-appengine.yaml

gcloud auth login bcliffor@canceridc.dev
gsutil cp test.openapi-appengine.yaml gs://webapp-deployment-files-idc-test/test.openapi-appengine.yaml
gcloud auth login bcliffor@systemsbiology.org