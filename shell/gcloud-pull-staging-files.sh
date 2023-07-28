mkdir ./json
mkdir ./txt

gsutil cp "gs://${DEPLOYMENT_BUCKET}/${ENV_FILE}" ./.env
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${API_RUNTIME_SA_KEY}" ./privatekey.json
#gsutil cp "gs://${DEPLOYMENT_BUCKET}/${OPEN_API_YAML}" ./openapi-appengine.yaml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${OPEN_API_YAML}" ./openapi-appengine.v1.yaml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${OPEN_API_YAML}" ./openapi-appengine.v2.yaml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${OPEN_API_YAML}" ./api/api.yaml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${API_APP_YAML}" ./app.yaml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${API_TOKEN_FILE}" ./api_token.txt

# Pack staged files for caching
echo "Packing JSON and text files for caching into deployment..."
cp --verbose *.json ./json
cp --verbose *.txt ./txt