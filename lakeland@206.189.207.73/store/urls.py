from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('view/<int:pk>/', views.view_product, name='view_product'),
    path('add/to/cart/', views.add_to_cart, name='add_to_cart'),
    path('process/order/', views.process_order, name='process_order'),
]
