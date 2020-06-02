import datetime

from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from license_service.models import Company, License
from main.response_processing import get_success_response
from main.sessions_storage import get_user
from user_service.models import User

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return round((dt - epoch).total_seconds() * 1000)


class UserView(APIView):
    def post(self, request):
        session = request.data["session"]
        company_name = get_user(session)
        company = Company.objects.filter(name=company_name)
        now = unix_time_millis(datetime.datetime.utcnow())

        if company:
            company = company[0]
            licences = License.objects.filter(company=company)
            data = []
            for licence in licences:
                licence_start_time = unix_time_millis(
                    datetime.datetime.utcfromtimestamp(licence.start_date.timestamp()))
                licence_end_time = unix_time_millis(
                    datetime.datetime.utcfromtimestamp(licence.end_date.timestamp()))
                data.append({
                    "from": licence_start_time,
                    "to": licence_end_time,
                    "peopleCount": licence.count_of_people
                })
            body = {
                "data": data,
                "currentServerTime": now
            }
            return get_success_response(body)
        else:
            return get_success_response({"status": 'out of company'})
