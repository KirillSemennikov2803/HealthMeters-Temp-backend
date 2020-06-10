import json

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User
from main import response_processing
from main.request_validation import validate_request
from main.response_processing import get_success_response, get_error_response, validate_response
from main.sessions_storage import authorize_user, validate_session, validate_license, get_user

req_schema_file = open('../schemas/edit_employee/request.json')
res_schema_file = open('../schemas/edit_employee/response.json')

req_schema = json.load(req_schema_file)
res_schema = json.load(res_schema_file)


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    @validate_license()
    def post(self, request):
        try:
            employee_guid = request.data["employeeGuid"]
            employee_data = request.data["employeeData"]

            user = User.objects.filter(guid=employee_guid)

            if not user:
                return validate_response({"status": "error",
                                          "reason": "outTgAccount"}, res_schema)

            full_name = employee_data["name"]
            tg_nick = employee_data["tgUsername"]
            position = employee_data["role"]

            user = user[0]

            user.full_name = full_name
            user.telegram_nick = tg_nick
            user.position = position

            check_full_name = User.objects.filter(full_name=full_name)
            check_telegram_nick = User.objects.filter(telegram_nick=tg_nick)
            if not check_full_name or not check_telegram_nick:
                return validate_response({"status": "usedTgAccount"}, res_schema)
            user.save()

            return validate_response({"status": "ok"}, res_schema)
        except:
            return get_error_response(500)
