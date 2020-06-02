from django.db import models


# Create your models here.

class Guid(models.Model):
    guid = models.CharField(max_length=36, unique=True)
    group = models.CharField(max_length=30)
    active = models.BooleanField(default=False)

    def set_active(self):
        self.active = True
        self.save()


class People(models.Model):
    guid = models.ForeignKey('Guid', related_name='users_to_guid', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default='student')
    login = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=32)

    def check_password(self, password):
        return self.password == password

    def get_role(self):
        return self.role
