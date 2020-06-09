from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User, ManageToUser
from main.response_processing import get_success_response, get_error_response
from main.sessions_storage import validate_session, validate_license


class UserView(APIView):
    @validate_session()
    @validate_license()
    def post(self, request):
        try:
            session = request.data["session"]
            worker_guid = request.data["workerGuid"]
            attached_manager = request.data["attachedManager"]

            manage_to_user_bd = ManageToUser.objects.filter(user=worker_guid)

            if manage_to_user_bd:
                manage_to_user_bd[0].delete()

            user = User.objects.filter(guid=worker_guid)
            manager = User.objects.filter(guid=attached_manager)

            if not user or not manager:
                return get_success_response({"status": "outTgAccount"})

            user = user[0]
            manager = manager[0]

            if user.company != manager.company:
                return get_success_response({"status": "error",
                                             "reason": "companyError"})

            manage_to_user_bd = ManageToUser.objects.create(user=user, manager=manager)
            return get_success_response({"status": "ok"})
        except:
            get_error_response(500)
