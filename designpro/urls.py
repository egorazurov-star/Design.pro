"""URL configuration for the Design.pro project."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Служебная админка Django (для разработчика)
    path('django-admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('studio.urls')),
]

# Раздача загруженных файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
