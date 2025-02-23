from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.product, name="product"),
    path('customer/<str:pk>', views.customer, name="customer"),
]