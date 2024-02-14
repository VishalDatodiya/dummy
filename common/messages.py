
"""All the messages that are sent to the server are sent to the client side."""


def get_login_success_message():
    return "Login successfully."

def get_login_failure_message():
    return "Invalid username or password."

def get_password_successfully_changed_message():
    return "Password is successfully changed."

def get_invalid_password_message():
    return "Current password is Invalid."

def get_old_and_new_password_same_message():
    return "Old and new password are same."

def get_password_mismatched_message():
    return "Password is not matched."

def get_failed_message():
    return "Something went wrong, please try again."

def get_password_successfully_reset_message():
    return "Password is successfully changed."

def get_refresh_token_required_message():
    return "Refresh token is required."

def get_invalid_refresh_token_message():
    return "Invalid or expired refresh token"

def get_success_message():
    return "Success"

def get_user_created_message():
    return "User is successfully created."

def get_user_already_created_message():
    return "User is already created."
