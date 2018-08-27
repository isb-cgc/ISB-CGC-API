mkdir ./json
mkdir ./txt

./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_APP_YAML}" ./app.yaml
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_SECRETS_FILE}" ./client_secrets.json
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_JSON_FILE}" ./privatekey.json

./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_DATASET_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${SERVICE_ACCOUNT_BLACKLIST_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${GOOGLE_ORG_WHITELIST_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${MANAGED_SERVICE_ACCOUNTS_JSON_FILE}" ./
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_DATASET_JSON_FILE}" ./

if [ -n "${PROD_NIH_AUTH_ON}" ]; then
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/saml/advanced_settings.json" ./saml/advanced_settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/saml/settings.json" ./saml/settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/saml/certs/cert.pem" ./saml/certs/cert.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/saml/certs/key.pem" ./saml/certs/key.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/NIH_FTP.txt" ./NIH_FTP.txt
fi

# Pack staged files for caching
cp --verbose *.json ./json
cp --verbose *.txt ./txt
