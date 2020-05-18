from rest_framework.views import APIView

from main.position_validate import validate_attach_admin
from main.response_processing import get_success_response
from user_service.models import User


class UserView(APIView):
    def post(self, request):
        telegram_id = request["telegram_id"]
        manager = request["manager_id"]
        worker = request["worker_id"]
        manager = User.objects.filter(telegram_id=manager)
        worker = User.objects.filter(telegram_id=worker)
        user = User.objects.filter(telegram_id=telegram_id)
        if not manager or not worker:
            return get_success_response({"status": "have not user"})
        manager = manager[0]
        worker = worker[0]
        if not validate_attach_admin(manager, worker):
            return get_success_response({"status": 'bad permission'})
