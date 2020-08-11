from django.shortcuts import render

from django.http import JsonResponse

from .models import Customer
from .models import Order
from .models import Product
from .models import OrderItem
from .models import ShippingAdress

import datetime

import json
# Create your views here.



from .utils import cookieCart
from .utils import cartData
from .utils  import guestOrder

def Store(request):
	data=cartData(request)
	cartItems=data['cartItems']

	products=Product.objects.all()
	context={'products':products,'cartItems':cartItems}
	return render(request,'store/store.html',context)

def Cart(request):
	data=cartData(request)
	items=data['items']
	order=data['order']
	cartItems=data['cartItems']
		

	context={'items':items,'order':order,'cartItems':cartItems}
	return render(request,'store/cart.html',context)

def Checkout(request):
	data=cartData(request)
	items=data['items']
	order=data['order']
	cartItems=data['cartItems']

	context={'items':items,'order':order,'cartItems':cartItems}
	return render(request,'store/checkout.html',context)


def UpdateItem(request):
	data=json.loads(request.body)
	productId=data['productId']
	action=data['action']

	customer = request.user.customer
	product=Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)



def ProcessOrder(request):
	transaction_id=datetime.datetime.now().timestamp()
	data=json.loads(request.body)


	if request.user.is_authenticated:
		customer=request.user.customer 
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		

		
	else:
		customer,order=guestOrder(request,data)
		
	total=float(data['form']['total'])
	order.transaction_id=transaction_id

	print("total",total)
	print("order total",order.get_cart_total)
		
	if  total==float(order.get_cart_total):
		order.complete=True
	order.save()

	if order.shipping==True:
			ShippingAdress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode']	
			)
	return JsonResponse("Payment Complete",safe=False)


def ViewOrders(request):
	username=request.user.customer
	order=Order.objects.filter(customer=username,complete=True)
	for orders in order:
		for orderitms in orders.orderitem_set.all():
			print(orderitms)
	context={'order':order}
	
	
	
	return render(request,'store/ordermade.html',context)