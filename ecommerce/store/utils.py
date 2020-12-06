from django.views.decorators.csrf import csrf_exempt
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

	else:
		try:
			cart = json.loads(request.COOKIES["cart"])
		except:
			cart = {}

		for i in cart:
			try:
				product = Product.objects.get(id = i)

				if product.digital == False:
					shipping = True

				item = {
					'product':{
						'id':i,
						'name': product.name,
						'price': product.price, 
						'digital': product.digital,
						'image': product.image,
					},
					'quantity': cart[i]['quantity'],
					'total_price': cart[i]['quantity'] * product.price,
				}
				total_quantity += cart[i]['quantity']
				total_price += cart[i]['quantity'] * product.price

				orderitems.append(item)
			except:
				pass

	return {"orderitems": orderitems,"total_quantity": total_quantity, "total_price": total_price, "shipping": shipping}



@csrf_exempt
def process_order(request):
	transaction_id = datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		get_cart_total = cart_total(request)["total_price"]
		order.transaction_id = transaction_id

		#if get_cart_total == float(data['form']['total']):

	else:
		customer, created = Customer.objects.get_or_create( name = data['form']['name'], email = data['form']['email'])
		order = Order.objects.create(customer = customer, complete = False)
		order.transaction_id = transaction_id
		items =  cart_total(request)["orderitems"]


		for item in items:

			orderitem = OrderItem.objects.create(
				product = Product.objects.get(id = item['product']['id'] ),
				order = order,
				quantity = item['quantity'],
				)
			orderitem.save()

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

	return JsonResponse('payment complete', safe=False)




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
