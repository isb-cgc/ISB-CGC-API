#./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/staging.env" ./.env
#./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/staging-ssl/client-cert.pem" ./client-cert.pem
#./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/staging-ssl/client-key.pem" ./client-key.pem
#./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/staging-ssl/server-ca.pem" ./server-ca.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/${TEST_APP_YAML}" ./app.yaml
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/${TEST_CERT_FILE}" ./client-cert.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/${TEST_KEY_FILE}" ./client-key.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/${TEST_CA_FILE}" ./server-ca.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/${TEST_SECRETS_FILE}" ./client_secrets.json
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/${TEST_PEM_FILE}" ./privatekey.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_TEST}/${TEST_OAUTH_TOKEN}" ~/.appcfg_oauth2_tokens
if [ -n "${TEST_NIH_AUTH_ON}" ]; then
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/dev-files/saml/advanced_settings.json" ./saml/advanced_settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/dev-files/saml/settings.json" ./saml/settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/dev-files/saml/certs/cert.pem" ./saml/certs/cert.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/dev-files/saml/certs/key.pem" ./saml/certs/key.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/dev-files/NIH_FTP.txt" ./NIH_FTP.txt
fi
