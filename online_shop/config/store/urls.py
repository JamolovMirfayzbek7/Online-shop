from django.urls import path
from .views import *
 
urlpatterns = [

    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('shop/', shop, name='shop'),
    path('detail/<int:pk>', detail, name='detail'),
    path('orders/', orders, name='orders'),
    path('create_order/', create_order, name='create_order'),
    path('rate_product/<int:pk>', rate_product, name='rate_product'),
    path('delete_cart/<int:pk>/', delete_cart_item, name='delete_cart_item'),
    path('edit_cart/<int:pk>/', edit_cart_item, name='edit_cart_item'),
]
