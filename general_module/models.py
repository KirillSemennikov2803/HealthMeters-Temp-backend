from django.db import models

from django.contrib import admin


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=36, unique=True)
    password_hash = models.CharField(max_length=36)
    active_people = models.IntegerField(default=1)

    def __str__(self):
        return self.name


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "active_people")


class License(models.Model):
    company = models.ForeignKey("general_module.Company", on_delete=models.CASCADE,
                                related_name="License_to_company")
    start_date = models.DateField()
    end_date = models.DateField()
    count_of_people = models.IntegerField()


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("company", "active_people", "start_date", "end_date", "count_of_people")


class AdminLicense(models.Model):
    token = models.CharField(max_length=32)
    company = models.ForeignKey("general_module.Company", on_delete=models.CASCADE,
                                related_name="admin_license_to_company", null=True, blank=True)
    active = models.BooleanField(default=True)


class User(models.Model):
    guid = models.CharField(max_length=36, primary_key=True)
    telegram_id = models.CharField(max_length=36, unique=True, null=True, blank=True)
    company = models.ForeignKey("license_service.Company", on_delete=models.CASCADE,
                                related_name="User_to_company")
    telegram_nick = models.CharField(max_length=36, unique=True)
    positions = [
        ('god', 'god'),
        ('admin', 'admin'),
        ('manager', 'manager'),
        ('worker', 'worker'),
    ]
    position = models.CharField(choices=positions, max_length=36)
    full_name = models.CharField(max_length=36)

    def __str__(self):
        return self.telegram_nick


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "position", "full_name")


class ManageToUser(models.Model):
    manager = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                                related_name="manage_to_user")
    user = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                             related_name="user_to_user")


@admin.register(ManageToUser)
class ManagerToUserAdmin(admin.ModelAdmin):
    list_display = ("manager", "user")


class HealthData(models.Model):
    user = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                             related_name="healthData_to_user")
    temperature = models.FloatField()
    date = models.DateTimeField()
    get_latest_by = "date"


@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ("user", "temperature", "date")
