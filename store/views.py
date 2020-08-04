from django.shortcuts import render


from .models import Customer
from .models import Order
from .models import Product
from .models import OrderItem
from .models import ShippingAdress
# Create your views here.


def Store(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'store/store.html',context)

def Cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0 }
    context={'items':items,'order':order}
    return render(request,'store/cart.html',context)

def Checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0 }
    context={'items':items,'order':order}
    return render(request,'store/checkout.html',context)
