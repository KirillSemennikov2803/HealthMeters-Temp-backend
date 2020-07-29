import configparser
from typing import List

import requests

from general_module.models import Employee
from main.request_proccessing import send_request, RequestType

config = configparser.ConfigParser()
config.read("config.ini")

bot_url = config["Hosts"]["tg_bot_url"]
headers = {
    'content-type': "application/json",
}

all_data_updated: bool = False


def send_new_employees(employees: List[Employee]) -> requests.codes:
    try:
        global all_data_updated
        payload: dict = {"data": []}

        for employee in employees:
            payload["data"].append({"guid": employee.guid, "nickname": employee.tg_username})

        response = send_request(RequestType.Post, bot_url, headers, payload)

        if response.status_code != requests.codes.ok:
            all_data_updated = False
            return response.status_code

        if not all_data_updated:
            synchronize_data()

        return response.status_code
    except:
        all_data_updated = False
        return requests.codes.server_error


def synchronize_data() -> None:
    global all_data_updated
    all_data_updated = True

    employees = Employee.objects.filter(telegram_id__isnull=True)

    employees_list: List[Employee] = []

    for employee in employees:
        employees_list.append(employee)

    status_code = send_new_employees(employees_list)

    if status_code != requests.codes.ok:
        all_data_updated = False
