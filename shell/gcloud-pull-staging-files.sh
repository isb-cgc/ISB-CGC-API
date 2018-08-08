mkdir ./json
mkdir ./txt

./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${TEST_API_APP_YAML}" ./app.yaml
./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${TEST_SECRETS_FILE}" ./client_secrets.json
./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${TEST_JSON_FILE}" ./privatekey.json
./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${TEST_USER_GCP_KEY}" ./

./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${SERVICE_ACCOUNT_BLACKLIST_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${GOOGLE_ORG_WHITELIST_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${MANAGED_SERVICE_ACCOUNTS_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${TEST_DATASET_JSON_FILE}" ./

if [ -n "${TEST_NIH_AUTH_ON}" ]; then
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/saml/advanced_settings.json" ./saml/advanced_settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/saml/settings.json" ./saml/settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/saml/certs/cert.pem" ./saml/certs/cert.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/saml/certs/key.pem" ./saml/certs/key.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/NIH_FTP.txt" ./NIH_FTP.txt
fi

# Pack staged files for caching
cp --verbose *.json ./json
cp --verbose *.txt ./txt
