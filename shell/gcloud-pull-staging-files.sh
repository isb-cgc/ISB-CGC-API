./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${TEST_API_APP_YAML}" ./app.yaml
./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${TEST_SECRETS_FILE}" ./client_secrets.json
./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/${TEST_PEM_FILE}" ./privatekey.pem

if [ -n "${TEST_NIH_AUTH_ON}" ]; then
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/saml/advanced_settings.json" ./saml/advanced_settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/saml/settings.json" ./saml/settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/saml/certs/cert.pem" ./saml/certs/cert.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/saml/certs/key.pem" ./saml/certs/key.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${TEST_GCLOUD_BUCKET}/NIH_FTP.txt" ./NIH_FTP.txt
fi
