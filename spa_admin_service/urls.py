
from django.urls import path

from spa_admin_service.views import \
    company_view, get_employees_data_view, delete_employee_view, edit_employee_view, \
    get_employees_view, authorize_view, register_view, licence_view, add_employee_view

app_name = "spa_admin_service"

urlpatterns = [
    path('company', company_view.UserView.as_view()),
    path('get_employees_data', get_employees_data_view.UserView.as_view()),
    path('delete_employee', delete_employee_view.UserView.as_view()),
    path('edit_employee', edit_employee_view.UserView.as_view()),
    path('get_employees', get_employees_view.UserView.as_view()),
    path('authorize', authorize_view.UserView.as_view()),
    path('register', register_view.UserView.as_view()),
    path('licence', licence_view.UserView.as_view()),
    path('add_employee', add_employee_view.UserView.as_view()),
]
