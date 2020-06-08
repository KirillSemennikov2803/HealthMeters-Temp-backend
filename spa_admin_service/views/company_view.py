import datetime

from rest_framework.views import APIView

from general_module.models import AdminLicense, Company, User, ManageToUser, License
from main.response_processing import get_success_response, get_error_response, get_unauthorized_response
from main.sessions_storage import validate_session, validate_license, get_user


class UserView(APIView):
    @validate_session
    def post(self, request):
        session = request.data["session"]
        company_name = get_user(session)

        company = Company.objects.filter(name=company_name)

        if not company:
            return get_unauthorized_response()

        company = company[0]

        now = datetime.datetime.utcnow()
        license_bd = License.objects.filter(company=company, start_date__lte=now, end_date__gte=now)

        current_licence = None

        if license_bd:
            current_licence = {
                "startTime": license_bd.start_date,
                "endTime": license_bd.end_date,
                "workersCount": license_bd.count_of_people
            }

        return get_success_response({"companyName": company.name,
                                     "attachedWorkersCount": company.active_people,
                                     "currentLicence": current_licence})
