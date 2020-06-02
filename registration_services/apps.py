import re

from django.apps import AppConfig
from rest_framework.response import Response
import json
from diht_feedback_collector.apps import setup_cors_response_headers, get_response_error_string_by_type


class RegistrationServiceConfig(AppConfig):
    name = 'registration_services'


def validate_registration_contract(req):
    try:
        user_data = req.data

        if re.match("application/json", req.headers["Content-Type"]) is None:
            return False

        if len(user_data.keys()) != 4:
            return False

        all_needed_keys_exist = \
            "token" in user_data.keys() \
            and "login" in user_data.keys() \
            and "password" in user_data.keys() \
            and "confirmation" in user_data.keys()

        all_types_valid = \
            isinstance(user_data["token"], str) \
            and isinstance(user_data["login"], str) \
            and isinstance(user_data["password"], str) \
            and isinstance(user_data["confirmation"], str)

        return all_needed_keys_exist and all_types_valid

    except Exception:
        return False


def validate_registration_data(token, login, password, confirmation):
    is_token_valid = \
        re.fullmatch("[a-z0-9]{8}[-][a-z0-9]{4}[-][a-z0-9]{4}[-][a-z0-9]{4}[-][a-z0-9]{12}", token) is not None

    is_login_valid = \
        re.fullmatch("[a-zA-Z0-9-]*", login) is not None \
        and len(login) >= 8

    is_password_valid = \
        re.fullmatch("[a-fA-F0-9]{32}", password) is not None

    is_confirmation_valid = \
        password == confirmation

    return is_token_valid and is_login_valid and is_password_valid and is_confirmation_valid


def get_registration_response_success(
        does_token_exist,
        is_token_unactivated,
        is_login_unique
):
    body = {
        "doesTokenExist": does_token_exist,
        "isTokenUnactivated": is_token_unactivated,
        "isLoginUnique": is_login_unique
    }

    return setup_cors_response_headers(Response(body, status=200, content_type="application/json"))


def get_registration_response_error(error_type, status_code):
    body = {
        "errorType": get_response_error_string_by_type(error_type)
    }

    return setup_cors_response_headers(Response(body, status=status_code, content_type="application/json"))
