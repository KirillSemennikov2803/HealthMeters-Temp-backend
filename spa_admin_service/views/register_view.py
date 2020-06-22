from rest_framework.views import APIView

from general_module.models import AdminPanelLicence, Company

from main.request_validation import validate_request
from main.response_processing import server_error_response, cors_response, validate_response

from spa_admin_service.schemas.register.request import req_schema
from spa_admin_service.schemas.register.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    def post(self, request):
        try:
            token = request.data["token"]
            company_name = request.data["companyName"]
            password = request.data["password"]

            admin_panel_licence = AdminPanelLicence.objects.filter(token=token)

            if admin_panel_licence:
                return validate_response({
                    "status": "error",
                    "reason": "invalidToken"
                }, res_schema)

            else:
                admin_panel_licence = admin_panel_licence[0]

            if admin_panel_licence.activated:
                return validate_response({
                    "status": "error",
                    "reason": "activatedToken"
                }, res_schema)

            if Company.objects.filter(name=company_name) is not None:
                return validate_response({
                    "status": "error",
                    "reason": "usedCompanyName"
                }, res_schema)

            admin_panel_licence.activated = True
            admin_panel_licence.save()

            Company.objects.create(name=company_name, password_hash=password)
            return validate_response({"status": "ok"}, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
