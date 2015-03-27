from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from registration.models import UserForm
from django.http import HttpResponseRedirect

def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('login')
    else:
        form = UserForm() 

    return render(request, 'registration/add_user.html', {'form': form}) 

def login(request):
	render(request, 'registration/login.html')