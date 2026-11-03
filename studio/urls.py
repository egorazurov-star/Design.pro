from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('requests/create/', views.request_create, name='request_create'),
    path('superadmin/', views.admin_panel, name='superadmin'),
]
