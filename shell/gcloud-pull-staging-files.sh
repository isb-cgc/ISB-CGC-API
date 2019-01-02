mkdir ./json
mkdir ./txt

./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/${DEV_API_APP_YAML}" ./app.yaml
./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/${DEV_SECRETS_FILE}" ./client_secrets.json
./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/${DEV_JSON_FILE}" ./privatekey.json

./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/${SERVICE_ACCOUNT_BLACKLIST_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/${GOOGLE_ORG_WHITELIST_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/${MANAGED_SERVICE_ACCOUNTS_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/${DEV_DATASET_JSON_FILE}" ./


# Pack staged files for caching
cp --verbose *.json ./json
cp --verbose *.txt ./txt
