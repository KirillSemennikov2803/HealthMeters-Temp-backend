from rest_framework.views import APIView

from general_module.models import Employee, ManagerToWorker
from main.response_processing import get_success_response, get_error_response


def validate_company_context_attach(admin: Employee, manager: Employee, worker: Employee):
    return admin.company == manager.company == worker.company


class UserView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data["telegram_id"]
            manager_id = request.data["manager_id"]
            worker_id = request.data["worker_id"]
            manager = Employee.objects.filter(telegram_id=manager_id)
            worker = Employee.objects.filter(telegram_id=worker_id)
            user = Employee.objects.filter(telegram_id=telegram_id)[0]
            if not manager or not worker:
                return get_success_response({"status": "have not user"})
            manager = manager[0]
            worker = worker[0]
            if not (manager.role == "manager" and worker.role == "worker"):
                return get_success_response({"status": 'bad permission'})
            if not validate_company_context_attach(user, manager, worker):
                return get_success_response({"status": 'people in different company'})
            ManagerToWorker.objects.create(manager=manager, user=worker)
            return get_success_response({"status": 'ok'})
        except:
            return get_error_response(500)
