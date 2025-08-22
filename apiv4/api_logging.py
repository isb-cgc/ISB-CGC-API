from django.conf import settings
from google_helpers.stackdriver import StackDriverLogger
from flask import jsonify


def make_deprecated_msg():
    response = jsonify({
        'code': 405,
        'message': 'ISB-CGC APi Endpoints have been deprecated.',
        'documentation': 'SwaggerUI interface available at <{}/swagger/>.'.format(settings.BASE_API_URL) +
                         'Historical documentation available at <https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/progAPI-v4/Programmatic-Demo.html>'
    })
    response.status_code = 405
    return response


# Log all API activity to StackDriver
st_logger = StackDriverLogger.build_from_django_settings()
log_name = settings.API_ACTIVITY_LOG_NAME
user_activity_message = "[USER API CALL] User {} performing method {} path {}"
activity_message = "[API CALL] Saw method {} for path {}"