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
    company = models.ForeignKey("license_service.Company", on_delete=models.CASCADE,
                                related_name="License_to_company")
    start_date = models.DateField()
    end_date = models.DateField()
    count_of_people = models.IntegerField()


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("company", "active_people", "start_date", "end_date", "count_of_people")
