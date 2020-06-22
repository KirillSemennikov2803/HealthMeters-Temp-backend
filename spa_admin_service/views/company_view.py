import datetime

from rest_framework.views import APIView

from general_module.models import Company, Licence
from main.request_validation import validate_request
from main.response_processing import validate_response, get_error_response
from main.sessions_storage import validate_session, get_user
from spa_admin_service.schemas.company.request import req_schema
from spa_admin_service.schemas.company.response import res_schema


class UserView(APIView):
    @validate_request(req_schema)
    @validate_session()
    def post(self, request):
        try:
            session = request.data["session"]
            company = Company.objects.filter(guid=get_user(session))[0]
            now = datetime.datetime.utcnow()

            licence_active = \
                Licence.objects.filter(company=company, start_date__lte=now, end_date__gte=now) \
                is not None

            return validate_response({
                "companyName": company.name,
                "licenceActive": licence_active
            }, res_schema)
        except:
            return get_error_response(500)
