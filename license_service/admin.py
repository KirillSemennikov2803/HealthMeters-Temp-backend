from django.contrib import admin

# Register your models here.
from license_service.models import CompanyLicense, Company, License, RenewalLicense

admin.site.register(Company)
admin.site.register(CompanyLicense)
admin.site.register(License)
admin.site.register(RenewalLicense)
