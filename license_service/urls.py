from django.urls import path
from .views import UserView

app_name = "license_service"

urlpatterns = [
    path('', UserView.as_view()),
]
