from stackdriver_logging import StackDriverLogger
from apiv4 import API_ACTIVITY_LOG_NAME, GCLOUD_PROJECT_ID

# Log all API activity to StackDriver
st_logger = StackDriverLogger(GCLOUD_PROJECT_ID)
log_name = API_ACTIVITY_LOG_NAME
user_activity_message = "[USER API CALL] User {} performing method {} path {}"
activity_message = "[API CALL] Saw method {} for path {}"

