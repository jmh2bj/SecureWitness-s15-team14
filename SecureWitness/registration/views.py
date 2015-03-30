from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import Permission, User, Group
from registration.models import UserForm, GroupForm
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
	elif request.user.is_authenticated():
		return HttpResponseRedirect('confirm')
	else:
		form = UserForm()
	return render(request, 'registration/login.html', {'form': form})

def confirm(request):
	# how to add permissions to a user
	# admin = Permission.objects.get(codename='admin')
	# if request.user.is_authenticated():
	# 	youser = User.objects.get(username=request.user.username)
	# 	youser.user_permissions = [admin]
	permissions = ""
	if not request.user.is_authenticated():
		permissions = "no user logged in"
	else:
		permissions = str(request.user.get_all_permissions())
	
	return render(request, 'registration/confirm.html', {'permissions': permissions})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('login')

def groups(request):
	if request.method == "POST":
		Group.objects.create(request.POST['name'])
	info = {}
	if not request.user.is_authenticated():
		info['groups'] = ["no user logged in"]
	else:
		if request.user.has_perm('registration.admin'):
			info['admin'] = True
			info['groups'] = Group.objects.all()
			info['form'] = GroupForm
		else:
			info['groups'] = request.user.groups

	return render(request, 'groups.html', info)

def groupinfo(request, groupname):
	return HttpResponse(Group.objects.get(name=groupname))
