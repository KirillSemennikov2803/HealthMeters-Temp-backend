from enum import Enum

import requests
from requests import Response


class RequestType(Enum):
    Post = "POST"
    Get = "Get"


def send_request(type_request: RequestType, url: str, headers: dict, payload: str) -> Response:
    response = requests.request(type_request.value, url, headers=headers, data=payload)
    return response
