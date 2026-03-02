# apps/core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('hakkimizda/', views.about, name='about'),
    path('sertifikalar/', views.certificates, name='certificates'),
]
