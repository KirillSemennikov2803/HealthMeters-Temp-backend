from django.urls import path

from . import views

app_name = "deploy"

urlpatterns = [
    path('add_user', views.UserView().as_view()),
]
