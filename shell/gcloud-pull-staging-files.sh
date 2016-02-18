#./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/staging.env" ./.env
#./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/staging-ssl/client-cert.pem" ./client-cert.pem
#./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/staging-ssl/client-key.pem" ./client-key.pem
#./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/staging-ssl/server-ca.pem" ./server-ca.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_APP_YAML}" ./app.yaml
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_CERT_FILE}" ./client-cert.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_KEY_FILE}" ./client-key.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_CA_FILE}" ./server-ca.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_SECRETS_FILE}" ./client_secrets.json
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${PROD_PEM_FILE}" ./privatekey.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/${DEV_OAUTH_TOKEN}" ~/.appcfg_oauth2_tokens
if [ -n "${PROD_NIH_AUTH_ON}" ]; then
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/prod-files/saml/advanced_settings.json" ./saml/advanced_settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/prod-files/saml/settings.json" ./saml/settings.json
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/prod-files/saml/certs/cert.pem" ./saml/certs/cert.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/prod-files/saml/certs/key.pem" ./saml/certs/key.pem
  ./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET}/prod-files/NIH_FTP.txt" ./NIH_FTP.txt
fi
