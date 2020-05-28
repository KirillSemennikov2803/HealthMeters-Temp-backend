from django.db import models


# Create your models here.

class Company(models.Model):
    license = models.OneToOneField("license_service.CompanyLicense", on_delete=models.CASCADE,
                                   related_name="company_to_license")
    active_people = models.IntegerField(default=1)


class CompanyLicense(models.Model):
    company = models.OneToOneField("license_service.Company", on_delete=models.CASCADE,
                                   related_name="company_license_to_company")
    end_time = models.DateField(null=True)
    count_of_people = models.IntegerField()


class License(models.Model):
    active = models.BooleanField(default=True)
    key = models.CharField(max_length=16)
    # count of days
    duration = models.IntegerField()
    count_of_people = models.IntegerField()


class RenewalLicense(models.Model):
    active = models.BooleanField(default=True)
    key = models.CharField(max_length=16)
    # count of days
    duration = models.IntegerField()
    delta_people = models.IntegerField(default=0)
    pass
