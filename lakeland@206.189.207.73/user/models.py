from django.db import models
import random
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models.signals import pre_save, post_save


def username_genertor(instance, sender, *args, **kwargs):
	username = instance.first_name +'_'+ instance.last_name 
	while User.objects.filter(username = username):
		username = username + str(random.randint(1,100))
	instance.username = username

pre_save.connect(username_genertor, sender = User)

class EmailBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):

		if '@' in username:
			kwargs = {'email': username}
		else:
			kwargs = {'username': username}

		try:
			user = User.objects.get(**kwargs)
		except UserModel.DoesNotExist:
			return None
		else:
			if user.check_password(password):
				return user
		return None
