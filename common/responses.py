
"""All the responses from the server should be sent to the client."""

from common import messages


def login_success_response(token):
    return {
        "message" : messages.get_login_success_message(),
        "code" : 200,
        "token" : token,
    }

def password_successfully_changed_response():
    return {
        "message" : messages.get_password_successfully_changed_message(),
        "code" : 200,
    }

def login_failed_response():
    return {
        "error" : messages.get_login_failure_message(),
        "code" : 400,
    }

def invalid_password_response():
    return {
        "error" : messages.get_invalid_password_message(),
        "code" : 400,
    }

def failed_response():
    return {
        "error" : messages.get_failed_message(),
        "code" : 400,
    }

def password_successfully_reset_response():
    return {
        "message" : messages.get_password_successfully_reset_message(),
        "code" : 200,
    }

def refresh_token_required_response():
    return {
        "message": messages.get_refresh_token_required_message(),
        "code": 200,
        "refresh": "",
    }

def refresh_token_invalid():
    return {
        "error": messages.get_invalid_refresh_token_message(),
        "code": 200,
    }

def user_created_response():
    return {
        "message": messages.get_user_created_message(),
        "code": 200,
    }

def success_response(data):
    return {
        "message": messages.get_success_message(),
        "code": 200,
        "results":data
    }

def success_response(data):
    return {
        "message": messages.get_success_message(),
        "code": 200,
        "results":data
    }

def user_already_created_response():
    return {
        "error": messages.get_user_already_created_message(),
        "code": 400,
    }
