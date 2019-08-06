gsutil cp gs://${DEPLOYMENT_BUCKET}/deployment_config.txt ./
if [ ! -f "deployment_config.txt" ]; then
  echo "[ERROR] Couldn't assign deployment configuration file - exiting."
  exit 1
fi