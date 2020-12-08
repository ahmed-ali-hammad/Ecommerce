from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
from datetime import datetime
from .utils import *



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





	




