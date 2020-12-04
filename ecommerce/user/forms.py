from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserAuthenticationForm (AuthenticationForm):
	username = forms.CharField(label='Email / Username') 



class UserRegisterationForm (UserCreationForm):
	first_name = forms.CharField(max_length=30)
	last_name  = forms.CharField(max_length=30)
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['first_name' ,'last_name', 'email', 'password1', 'password2']

