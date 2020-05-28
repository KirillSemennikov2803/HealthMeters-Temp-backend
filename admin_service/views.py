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
            _type = request.data["type"]
            telegram_id = request.data["telegram_id"]
            worker = request.data["worker"]
            telegram_worker = worker["telegram_id"]
            user = User.objects.filter(telegram_id=telegram_id)[0]
            company = user.company
            if _type == "add":
                position = worker['position']
                if not validate_admin_site_add_delete(position, user):
                    return get_success_response({"status": 'bad permission'})
                full_name = worker['full_name']
                nickname = worker['nickname']
                if company.license.count_of_people - company.active_people <= 0:
                    return get_success_response({"status": 'max people'})
                if len(User.objects.filter(telegram_id=telegram_worker)) > 0:
                    return get_success_response({"status": 'user already register'})
                User.objects.create(telegram_id=telegram_worker, company=company, position=position,
                                    full_name=full_name, telegram_nick=nickname)
                company.active_people += 1
                company.save()
                return get_success_response({"status": "ok"})
            if _type == "delete":
                worker_bd = User.objects.filter(telegram_id=telegram_worker)
                if not worker_bd:
                    return get_success_response({"status": "out user"})
                worker_bd = worker_bd[0]
                if worker_bd.company != user.company or not validate_admin_site_add_delete(worker_bd.position, user):
                    return get_success_response({"status": "bad permission"})

                worker_bd.delete()
                company.active_people -= 1
                company.save()
                return get_success_response({"status": "ok"})
            return get_error_response(500)
        except:
            return get_error_response(500)
