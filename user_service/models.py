from django.db import models

# Create your models here.
from django.contrib import admin


class User(models.Model):
    telegram_id = models.CharField(max_length=36, unique=True)
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
        return self.telegram_id


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "position", "full_name")


class ManageToUser(models.Model):
    manager = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                                related_name="manage_to_user")
    user = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                             related_name="user_to_user")


@admin.register(ManageToUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("manager", "user")


class HealthData(models.Model):
    user = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                             related_name="healthData_to_user")
    temperature = models.FloatField()
    date = models.DateTimeField()
    get_latest_by = "date"
