from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from registration.models import UserForm
from django.http import HttpResponseRedirect, HttpResponse

def add_user(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			newUser = User.objects.create_user(**form.cleaned_data)
            # redirect, or however you want to get to the main view
			return HttpResponseRedirect('confirm')
	else:
		form = UserForm() 

	return render(request, 'registration/add_user.html', {'form': form}) 

def login(request):
	if request.method == "POST":
		user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				auth.login(request, user)
		        # redirect, or however you want to get to the main view
				return HttpResponseRedirect('confirm')
			else:
				return HttpResponse('user disabled')
		else:
			form = UserForm()
			return render(request, 'registration/login.html', {'form': form, 'errors': True})
	else:
		form = UserForm()
	return render(request, 'registration/login.html', {'form': form})

def confirm(request):
	return render(request, 'registration/confirm.html', {'user': request.user})
