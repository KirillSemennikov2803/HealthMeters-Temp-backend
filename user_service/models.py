from django.db import models


# Create your models here.

class User(models.Model):
    telegram_id = models.CharField(max_length=36)
    company = models.ForeignKey("license_service.Company", on_delete=models.CASCADE,
                                related_name="User to company")
    position = models.CharField()
    full_name = models.CharField()


class ManageToUser(models.Model):
    manage = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                               related_name="manage to user")
    user = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                             related_name="user to user")


class HealthData(models.Model):
    user = models.ForeignKey("user_service.User", on_delete=models.CASCADE,
                             related_name="healthData to user")
    temperature = models.FloatField()
    date = models.DateTimeField()
    get_latest_by = "date"
