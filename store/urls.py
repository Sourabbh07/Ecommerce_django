

from django.urls import path

from .views import Store
from .views import Cart
from .views import Checkout


urlpatterns = [
    path('',Store,name='store'),
    path('cart/',Cart,name='cart'),
    path('checkout/',Checkout,name='checkout'),
    
    
]
