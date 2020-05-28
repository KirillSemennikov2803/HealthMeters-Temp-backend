from django.urls import path
from .views import UserView

app_name = "admin_service"

urlpatterns = [
    path('', UserView.as_view()),
]
