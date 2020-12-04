from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
from datetime import datetime

def cart_total(request):
	orderitems = []
	total_quantity = 0
	total_price = 0
	shipping = False
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		orderitems = OrderItem.objects.filter(order=order)

		for item in orderitems:
			total_quantity += item.quantity
		
		for item in orderitems:
			if item.product.digital == False:
				shipping = True
				break 

		for item in orderitems:
			total_price += item.quantity * item.product.price

	return {"orderitems": orderitems,"total_quantity": total_quantity, "total_price": total_price, "shipping": shipping}


def store(request):
	products = Product.objects.all()
	total_quantity  = cart_total(request)['total_quantity']
	context  = {"products": products, 'total_quantity':total_quantity} 
	return render (request,'store/store.html', context)


def cart(request):	
	context  = cart_total(request)
	return render (request,'store/cart.html', context)


def checkout(request):	
	context  = cart_total(request)

	return render (request,'store/checkout.html', context)


def view_product(request, pk):
	item = Product.objects.get(id=pk)
	total_quantity  = cart_total(request)['total_quantity']
	context = {'item':item, 'total_quantity':total_quantity}
	return render (request, "store/view_product.html", context)


def add_to_cart(request):
	data = json.loads(request.body)
	id = data["productid"]
	action = data["action"]
	print(action)
	customer = request.user.customer
	product = Product.objects.get(id=id)
	order, created = Order.objects.get_or_create(customer = customer, complete = False)

	cart_final, created = OrderItem.objects.get_or_create(product=product, order= order)
	if action == 'add':
		cart_final.quantity += 1
	elif action == 'remove':
		cart_final.quantity -= 1

	cart_final.save()

	if cart_final.quantity <= 0:
		cart_final.delete()

	total_quantity  = cart_total(request)['total_quantity']
	context  = {'total_quantity':total_quantity, 'orderitem_quantity':cart_final.quantity} 

	return JsonResponse(context)


def process_order(request):
	transaction_id = datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		get_cart_total = cart_total(request)["total_price"]
		order.transaction_id = transaction_id

		#if get_cart_total == float(data['form']['total']):
		order.complete = True
		order.save()

		if cart_total(request)['shipping'] == True:
			ShippingAddress.objects.create(
				customer     = customer,
				order        = order,
				address      = data['shipping']['address'],
				city         = data['shipping']['city'],
				state        = data['shipping']['state'],
				zip_code     = data['shipping']['zipcode'],
			)
	else:
		print ('user is not logged in')

	return JsonResponse('payment complete', safe=False)
	




