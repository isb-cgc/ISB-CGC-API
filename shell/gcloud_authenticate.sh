echo $TEST_PRIVATE_KEY_FOR_V2 | base64 --decode --ignore-garbage > deployment.key.json

/home/circleci/${CIRCLE_PROJECT_REPONAME}/google-cloud-sdk/bin/gcloud auth activate-service-account --key-file deployment.key.json
/home/circleci/${CIRCLE_PROJECT_REPONAME}/google-cloud-sdk/bin/gcloud config set account $TEST_CLIENT_EMAIL
/home/circleci/${CIRCLE_PROJECT_REPONAME}/google-cloud-sdk/bin/gcloud config set project "$TEST_PROJECT_ID"
