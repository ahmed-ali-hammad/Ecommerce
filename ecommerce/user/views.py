from django.shortcuts import render, redirect
from django.contrib.auth import login
from . import forms



def login_view(request):
	if request.method == 'POST':
		form = forms.UserAuthenticationForm(data = request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect ('store') 
	else:
		form = forms.UserAuthenticationForm()
	return render (request, 'user/login.html', {'form': form})



def register_view(request):
	if request.method == 'POST':
		form = forms.UserRegisterationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect ('store') 
	else:
		form = forms.UserRegisterationForm()
	return render (request, 'user/register.html', {'form': form})





