"""HealthMeters URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin_db/', admin.site.urls),
    path('admin/', include('admin_service.urls')),
    path('attach/', include('attach_service.urls')),
    path('license/', include('license_service.urls')),
    path('list/', include('list_of_people_service.urls')),
    path('manage/', include('manage_service.urls')),
    path('statistic/', include('statistics_service.urls')),
    path('user/', include('user_service.urls')),
    path('position/', include('user_position_service.urls')),
]
