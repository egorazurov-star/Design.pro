"""URL configuration for the Design.pro project."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Служебная админка Django (для разработчика)
    path('django-admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('studio.urls')),
]
