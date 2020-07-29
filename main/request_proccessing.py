from enum import Enum


import requests
from requests import Response


class RequestType(Enum):
    Post = "POST"
    Get = "GET"


def send_request(request_type: RequestType, url: str, headers: dict, payload: dict) -> Response:
    response = requests.request(request_type.value, url, headers=headers, data=payload)
    return response
