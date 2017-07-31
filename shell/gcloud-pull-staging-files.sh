./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_APP_YAML}" ./app.yaml
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_SECRETS_FILE}" ./client_secrets.json
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_JSON_FILE}" ./privatekey.json

./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/${DEV_DATASET_JSON_FILE}" ./

if [ -n "${DEV_NIH_AUTH_ON}" ]; then
  ./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/saml/advanced_settings.json" ./saml/advanced_settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/saml/settings.json" ./saml/settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/saml/certs/cert.pem" ./saml/certs/cert.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/saml/certs/key.pem" ./saml/certs/key.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${DEV_GCLOUD_BUCKET}/NIH_FTP.txt" ./NIH_FTP.txt
if [ -n "${PROD_NIH_AUTH_ON}" ]; then
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/saml/advanced_settings.json" ./saml/advanced_settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/saml/settings.json" ./saml/settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/saml/certs/cert.pem" ./saml/certs/cert.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/saml/certs/key.pem" ./saml/certs/key.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/NIH_FTP.txt" ./NIH_FTP.txt
fi
