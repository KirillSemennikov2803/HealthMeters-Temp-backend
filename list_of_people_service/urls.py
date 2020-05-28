from django.urls import path
from .views import UserView

app_name = "list_of_people_service"

urlpatterns = [
    path('', UserView.as_view()),
]
