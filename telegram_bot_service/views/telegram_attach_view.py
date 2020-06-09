from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from general_module.models import User, ManageToUser
from main.position_validate import validate_attach_admin, validate_company_context_attach
from main.response_processing import get_success_response, get_error_response


class UserView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data["telegram_id"]
            manager_id = request.data["manager_id"]
            worker_id = request.data["worker_id"]
            manager = User.objects.filter(telegram_id=manager_id)
            worker = User.objects.filter(telegram_id=worker_id)
            user = User.objects.filter(telegram_id=telegram_id)[0]
            if not manager or not worker:
                return get_success_response({"status": "have not user"})
            manager = manager[0]
            worker = worker[0]
            if not validate_attach_admin(manager, worker):
                return get_success_response({"status": 'bad permission'})
            if not validate_company_context_attach(user, manager, worker):
                return get_success_response({"status": 'people in different company'})
            ManageToUser.objects.create(manager=manager, user=worker)
            return get_success_response({"status": 'ok'})
        except:
            return get_error_response(500)
