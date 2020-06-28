from rest_framework.views import APIView

from general_module.models import Company

from main.request_validation import validate_request
from main.response_processing import validate_response, server_error_response, cors_response
from main.session_storage import get_user
from main.request_validation import validate_session
from main.licence_packs_managment import get_active_licence_pack

from spa_admin_service.schemas.company.request import req_schema
from spa_admin_service.schemas.company.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    def post(self, request):
        try:
            session = request.data["session"]
            company = Company.objects.filter(guid=get_user(session))[0]

            return validate_response({
                "companyName": company.name,
                "licenceActive": get_active_licence_pack(company) is not None
            }, res_schema)
        except:
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
