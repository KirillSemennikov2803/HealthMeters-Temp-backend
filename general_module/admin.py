from django.contrib import admin

from general_module.models import \
    Company, Licence, Employee, ManagerToWorker, HealthData, AdminPanelLicence


@admin.register(Company)
class CompanyRegistered(admin.ModelAdmin):
    list_display = ("name", "guid", "employees_count")


@admin.register(Licence)
class LicenceRegistered(admin.ModelAdmin):
    list_display = ("company", "start_time", "end_time", "employees_count")


@admin.register(Employee)
class EmployeeRegistered(admin.ModelAdmin):
    list_display = ("initials", "role", "guid", "tg_username", "telegram_id")


@admin.register(ManagerToWorker)
class ManagerToWorkerRegistered(admin.ModelAdmin):
    list_display = ("manager", "worker")


@admin.register(AdminPanelLicence)
class AdminPanelLicenceRegistered(admin.ModelAdmin):
    list_display = ("company", "token", "activated")


@admin.register(HealthData)
class HealthDataRegistered(admin.ModelAdmin):
    list_display = ("employee", "temperature", "date")
