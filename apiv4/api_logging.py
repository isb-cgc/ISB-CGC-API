from google_helpers.stackdriver import StackDriverLogger
from apiv4 import API_ACTIVITY_LOG_NAME


# Log all API activity to StackDriver
st_logger = StackDriverLogger.build_from_django_settings()
log_name = API_ACTIVITY_LOG_NAME
user_activity_message = "[USER API CALL] User {} performing method {} path {}"
activity_message = "[API CALL] Saw method {} for path {}"