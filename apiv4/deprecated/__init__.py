
from flask import jsonify, request

HTTP_405_METHOD_NOT_ALLOWED = 405


def make_405_response(msg):
    response = jsonify({
        'code': HTTP_405_METHOD_NOT_ALLOWED,
        'message': msg
    })

    response.status_code = HTTP_405_METHOD_NOT_ALLOWED

    return response
