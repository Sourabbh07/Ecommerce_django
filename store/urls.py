

from django.urls import path

from .views import Store
from .views import Cart
from .views import Checkout
from .views import UpdateItem
from .views import ProcessOrder
from .views import ViewOrders

urlpatterns = [
    path('',Store,name='store'),
    path('cart/',Cart,name='cart'),
    path('checkout/',Checkout,name='checkout'),

    path('updateitem/',UpdateItem,name='updateitem'),

    path('processorder/',ProcessOrder,name='processorder'),
    path('vieworders/',ViewOrders,name='vieworders'),
    
    
]
