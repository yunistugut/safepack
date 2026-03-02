from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('tesekkurler/', views.contact_success, name='success'),
]
