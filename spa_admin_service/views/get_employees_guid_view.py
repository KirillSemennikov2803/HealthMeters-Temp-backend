from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User
from main.response_processing import get_success_response, get_error_response, get_unauthorized_response
from main.sessions_storage import validate_session, get_user, validate_license


class UserView(APIView):
    @validate_session()
    @validate_license()
    def post(self, request):
        try:
            session = request.data["session"]
            company_name = get_user(session)

            company = Company.objects.filter(name=company_name)

            if not company:
                return get_unauthorized_response()

            company = company[0]

            users = User.objects.filter(company=company)

            employees = []

            for user in users:
                employees.append(user.guid)

            return get_success_response({"status": "ok",
                                         "employees": employees})
        except:
            return get_error_response(500)
