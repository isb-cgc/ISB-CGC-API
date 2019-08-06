gsutil cp gs://${DEPLOYMENT_BUCKET}/deployment_config.txt ./
if [ ! -f "delpoyment_config.txt" ]; then
  echo "[ERROR] Couldn't assign deployment configuration file - exiting."
  exit 1
else
  xargs -a config_file.txt -I{} echo "export {}" >> $BASH_ENV
fi