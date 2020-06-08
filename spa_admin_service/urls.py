
from django.urls import path

from spa_admin_service.views import company_view, get_employees_data_view, delete_employee_view, edit_employee_view, \
    attach_worker_view, get_employees_guid_view, authorise_view, register_view

app_name = "spa_admin_service"

urlpatterns = [
    path('/company', company_view.UserView.as_view()),
    path('/get_employees_data', get_employees_data_view.UserView.as_view()),
    path('/delete_employee', delete_employee_view.UserView.as_view()),
    path('/edit_employee', edit_employee_view.UserView.as_view()),
    path('/attach_worker', attach_worker_view.UserView.as_view()),
    path('/get_employees', get_employees_guid_view.UserView.as_view()),
    path('/authorise', authorise_view.UserView.as_view()),
    path('/register', register_view.UserView.as_view()),
]