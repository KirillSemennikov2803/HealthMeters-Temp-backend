from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from license_service.models import Company
from main.position_validate import validate_admin_site_add_delete
from main.response_processing import get_success_response, get_error_response
from user_service.models import User


class UserView(APIView):
    def post(self, request):
        try:
            type = request["type"]
            telegram_id = request["telegram_id"]
            worker = request["worker"]
            telegram_worker = worker["telegram_id"]
            position = worker['position']
            full_name = worker['full_name']
            user = User.objects.filter(telegram_id=telegram_id)[0]
            if not validate_admin_site_add_delete(position, user):
                return get_success_response({"status": 'bad permission'})

            if type == "add":
                company = user.company
                if company.license.count_of_people - company.active_people <= 0:
                    return get_success_response({"status": 'max people'})
                User.objects.create(telegram_id=telegram_worker, company=company, position=position,
                                    full_name=full_name)
                return get_success_response({"status": "ok"})
            if type == "delete":
                worker_bd = User.objects.filter(telegram_id=telegram_worker)
                if not worker_bd:
                    return get_success_response({"status": "out user"})
                worker_bd[0].delete()
                return get_success_response({"status": "ok"})
            return get_error_response(500)
        except:
            return get_error_response(500)
