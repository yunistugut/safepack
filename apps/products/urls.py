from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # /urunler/
    path('', views.product_list, name='list'),

    # /urunler/is-eldivenleri/
    path('<slug:slug>/', views.category_detail, name='category'),

    # /urunler/is-eldivenleri/nitril-kapli-eldiven/
    path('<slug:category_slug>/<slug:slug>/', views.product_detail, name='detail'),
]
