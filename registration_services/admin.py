from django.contrib import admin

# Register your models here.

from .models import Guid, People

admin.site.register(Guid)
admin.site.register(People)
