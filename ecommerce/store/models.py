from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
	user  = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
	name  = models.CharField (max_length = 200, null = True)
	email = models.EmailField (max_length = 254, null = True)

	def __str__(self):
		return self.name


class Product (models.Model):
	name    = models.CharField (max_length = 200, null = True)
	price   = models.DecimalField(max_digits=10, decimal_places=2)
	digital = models.BooleanField (default = False, blank = True)
	image   = models.ImageField(default= 'images/product.png', blank = True)

	def __str__(self):
		return self.name


class Order (models.Model):
	customer       = models.ForeignKey (Customer, on_delete = models.SET_NULL ,null = True, blank = True)
	date_ordered   = models.DateTimeField (auto_now_add = True)
	complete       = models.BooleanField (default = False)
	transaction_id = models.CharField (max_length = 200, null = True)

	def __str__(self):
		return str(self.id)


class OrderItem (models.Model):
	product    = models.ForeignKey (Product, on_delete = models.SET_NULL ,null = True, blank = True)
	order      = models.ForeignKey (Order, on_delete = models.SET_NULL ,null = True, blank = True)
	quantity   = models.IntegerField (default = 0, null = True, blank = True)
	date_added = models.DateTimeField (auto_now_add = True)

	def total_price(self):
		self.total = self.quantity * self.product.price
		return self.total


class ShippingAddress (models.Model):
	customer     = models.ForeignKey ( Customer, on_delete = models.SET_NULL ,null = True)
	order        = models.ForeignKey (Order, on_delete = models.SET_NULL ,null = True)
	address      = models.CharField (max_length = 200, null = False)
	city         = models.CharField (max_length = 200, null = False)
	state        = models.CharField (max_length = 200, null = False)
	zip_code     = models.IntegerField (null = False)
	date_ordered = models.DateTimeField (auto_now_add = True)

	def __str__(self):
		return self.address