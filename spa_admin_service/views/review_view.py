from rest_framework.views import APIView
from django.core.mail import send_mail
from asgiref.sync import async_to_sync

from main.request_validation import validate_request
from main.response_processing import server_error_response, cors_response


class UserView(APIView):
    def post(self, request):
        # Todo:Настроить почтовый сервис https://tproger.ru/translations/email-functionality-django/
        try:
            data = request.data

            message = data["message"]
            rating = data["rating"]
            email = data["email"]
            name = data["name"]

            send_mail(
                'Subject here',
                'Here is the message.',
                'healthmeterstest@mail.ru',
                ['healthmeterstest@mail.ru'],
                fail_silently=False,
            )
        except Exception as err:
            print(err)
            return server_error_response()

    def options(self, request, *args, **kwargs):
        return cors_response()
