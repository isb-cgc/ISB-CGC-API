echo ${KEY} | base64 --decode --ignore-garbage > deployment.key.json

gcloud auth activate-service-account --key-file deployment.key.json
echo "Setting deployment client email to ${CLIENT_EMAIL}"
gcloud config set account $CLIENT_EMAIL
echo "Setting deployment project to ${PROJECT_ID}"
gcloud config set project "$PROJECT_ID"
