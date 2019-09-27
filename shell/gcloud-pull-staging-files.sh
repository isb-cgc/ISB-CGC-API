mkdir ./json
mkdir ./txt

gsutil cp "gs://${DEPLOYMENT_BUCKET}/${ENV_FILE}" ./.env
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${API_RUNTIME_SA_KEY}" ./privatekey.json
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${OPEN_API_YAML}" ./openapi-appengine.yaml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${OPEN_API_YAML}" ./apiv4/api.yaml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${API_APP_YAML}" ./app.yaml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${MONITORING_SA_KEY}" ./
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${DCF_SECRETS_FILE}" ./dcf_secrets.txt

gsutil cp "gs://${DEPLOYMENT_BUCKET}/${SERVICE_ACCOUNT_BLACKLIST_JSON_FILE}" ./
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${GOOGLE_ORG_WHITELIST_JSON_FILE}" ./
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${MANAGED_SERVICE_ACCOUNTS_JSON_FILE}" ./

# Pack staged files for caching
echo "Packing JSON and text files for caching into deployment..."
cp --verbose *.json ./json
cp --verbose *.txt ./txt