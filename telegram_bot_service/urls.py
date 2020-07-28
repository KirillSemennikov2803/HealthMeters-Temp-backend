from django.urls import path

from telegram_bot_service.views import manager_attached_workers_list, manager_attached_workers_statistics, \
    employee_role, worker_add_health_data_view, \
    company_list, synchronize_data, get_employee_tg_id

app_name = "telegram_bot_service"

urlpatterns = [
    path('role', employee_role.UserView().as_view()),
    path('attached_workers', manager_attached_workers_list.UserView().as_view()),
    path('attached_workers_statistics', manager_attached_workers_statistics.UserView().as_view()),
    path('add_health_data', worker_add_health_data_view.UserView().as_view()),
    path('companies', company_list.UserView().as_view()),
    path('synchronize', synchronize_data.UserView().as_view()),
    path('get_employee_tg_id', get_employee_tg_id.UserView().as_view()),
]
