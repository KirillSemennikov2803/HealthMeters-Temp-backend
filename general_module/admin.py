from django.contrib import admin

from general_module.models import \
    Company, Licence, Employee, ManagerToWorker, HealthData


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("guid", "name", "employees_count")


@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ("company", "start_time", "end_time", "employees_count")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "role", "initials")


@admin.register(ManagerToWorker)
class ManagerToWorkerAdmin(admin.ModelAdmin):
    list_display = ("manager", "worker")


@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ("employee", "temperature", "date")
