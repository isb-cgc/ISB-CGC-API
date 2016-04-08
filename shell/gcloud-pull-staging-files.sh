./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_UAT}/uat.env" ./.env
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_UAT}/ssl/ISB-CGC-uat-client-cert.pem" ./client-cert.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_UAT}/ssl/ISB-CGC-uat-client-key.pem" ./client-key.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_UAT}/ssl/ISB-CGC-uat-server-ca.pem" ./server-ca.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_UAT}/ISB-CGC-uat-client_secrets.json" ./client_secrets.json
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_UAT}/ISB-CGC-uat-privatekey2.json" ./privatekey.json
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_UAT}/ISB-CGC-uat-privatekey2.pem" ./privatekey.pem
./google-cloud-sdk/bin/gsutil cp "gs://${GCLOUD_BUCKET_UAT}/${DEV_OAUTH_TOKEN}" ~/.appcfg_oauth2_tokens