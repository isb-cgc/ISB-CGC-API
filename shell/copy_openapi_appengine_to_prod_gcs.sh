#!/bin/bash

#set -x

DATE=$(date '+%Y%m%d_%H%M%S')

cp openapi-appengine.v1.yaml prod.openapi-appengine.v1.yaml
sed -i "" 's/#host: "api.imaging.datacommons.cancer.gov"/host: "api.imaging.datacommons.cancer.gov"/' prod.openapi-appengine.v1.yaml
sed -i "" 's/x-google-audiences: "94/#x-google-audiences: "94/'  prod.openapi-appengine.v1.yaml
sed -i "" 's/#x-google-audiences: "19/x-google-audiences: "19/'  prod.openapi-appengine.v1.yaml
sed -i "" 's/#- "https"/- "https"/' prod.openapi-appengine.v1.yaml
sed -i "" 's/- "http"/#- "http"/' prod.openapi-appengine.v1.yaml
cp openapi-appengine.v2.yaml prod.openapi-appengine.v2.yaml
sed -i "" 's/#host: "api.imaging.datacommons.cancer.gov"/host: "api.imaging.datacommons.cancer.gov"/' prod.openapi-appengine.v2.yaml
sed -i "" 's/x-google-audiences: "94/#x-google-audiences: "94/'  prod.openapi-appengine.v2.yaml
sed -i "" 's/#x-google-audiences: "19/x-google-audiences: "19/'  prod.openapi-appengine.v2.yaml
sed -i "" 's/#- "https"/- "https"/' prod.openapi-appengine.v2.yaml
sed -i "" 's/- "http"/#- "http"/' prod.openapi-appengine.v2.yaml

gcloud auth login bcliffor@canceridc.dev
gsutil cp prod.openapi-appengine.v1.yaml gs://webapp-deployment-files-idc-prod/prod.openapi-appengine.v1.yaml
gsutil cp prod.openapi-appengine.v2.yaml gs://webapp-deployment-files-idc-prod/prod.openapi-appengine.v2.yaml
gcloud auth login bcliffor@systemsbiology.org