from django.db import models

from django.contrib import admin


class Company(models.Model):
    guid = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    employees_count = models.IntegerField(default=1)

    def __str__(self):
        return self.name


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("guid", "name", "employees_count")


class Licence(models.Model):
    company = models.ForeignKey(
        "general_module.Company", on_delete=models.CASCADE,
        related_name="licence_to_company")
    start_time = models.DateField()
    end_time = models.DateField()
    people_count = models.IntegerField()


@admin.register(Licence)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("company", "start_time", "end_time", "people_count")


class Employee(models.Model):
    guid = models.CharField(max_length=36, primary_key=True)
    telegram_id = models.CharField(max_length=36, unique=True, null=True, blank=True)
    company = models.ForeignKey(
        "general_module.Company", on_delete=models.CASCADE,
        related_name="employee_to_company")
    telegram_nick = models.CharField(max_length=36, unique=True)
    roles = [
        ('manager', 'manager'),
        ('worker', 'worker'),
    ]
    role = models.CharField(choices=roles, max_length=36)
    initials = models.CharField(max_length=36)

    def __str__(self):
        return self.telegram_nick


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "role", "initials")


class ManagerToWorker(models.Model):
    manager = models.ForeignKey(
        "general_module.Employee", on_delete=models.CASCADE,
        related_name="manager_to_worker")
    worker = models.ForeignKey(
        "general_module.Employee", on_delete=models.CASCADE,
        related_name="worker_to_worker")


@admin.register(ManagerToWorker)
class ManagerToWorkerAdmin(admin.ModelAdmin):
    list_display = ("manager", "worker")


class AdminPanelLicence(models.Model):
    token = models.CharField(max_length=32)
    company = models.ForeignKey(
        "general_module.Company", on_delete=models.CASCADE,
        related_name="admin_license_to_company", null=True, blank=True)
    active = models.BooleanField(default=True)


class HealthData(models.Model):
    employee = models.ForeignKey(
        "general_module.Employee", on_delete=models.CASCADE,
        related_name="health_data_to_employee")
    temperature = models.FloatField()
    date = models.DateTimeField()
    get_latest_by = "date"


@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ("employee", "temperature", "date")
