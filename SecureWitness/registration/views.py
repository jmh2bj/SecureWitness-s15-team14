from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import Permission, User, Group
from registration.models import UserForm, GroupForm, ReportForm, Report
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

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
	permissions = ""
	if not request.user.is_authenticated():
		permissions = "no user logged in"
	else:
		permissions = str(request.user.get_all_permissions())
	
	return render(request, 'registration/confirm.html', {'permissions': permissions})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('login')

def reports(request):
	info = {}
	if request.method == "POST" and request.user.is_authenticated():
		info['form'] = ReportForm(request.POST)
		newReport = Report.objects.create(owner=request.user, rep_title=request.POST['rep_title'], short_desc=request.POST['short_desc'], detailed_desc=request.POST['detailed_desc'], rep_date=request.POST['rep_date'], keywords=request.POST['keywords'], isPublic=request.POST['isPublic'])
		if 'file' in request.POST:
			newReport.file = request.POST['file']
		if 'allowed_groups' in request.POST:
			newReport.allowed_groups = request.POST['allowed_groups']
		if 'allowed_users' in request.POST:
			newReport.allowed_users = request.POST['allowed_users']
	else:
		info['form'] = ReportForm()
	if not request.user.is_authenticated():
		info['reports'] = ["no user logged in"]
		info['user'] = False
	else:
		info['user'] = True
		info['reports'] = Report.objects.filter(owner=request.user)

	return render(request, 'reports.html', info)

def reportinfo(request, pk):
	report = get_object_or_404(Report, pk=pk)
	info = {}
	if request.method == "POST" and request.user.is_authenticated() and report.owner == request.user:
		placeholder = "update reports here"
		#update reports
	if report.owner == request.user:
		info['form'] = ReportForm(instance=report)
	else:
		return HttpResponseForbidden("forbidden")
	return render(request, 'reportinfo.html', info)

def groups(request):
	if request.method == "POST" and request.user.is_superuser:
		Group.objects.create(name=request.POST['name'])
	info = {}
	if not request.user.is_authenticated():
		info['groups'] = ["no user logged in"]
	else:
		if request.user.is_superuser:
			info['admin'] = True
			info['groups'] = Group.objects.all()
			info['form'] = GroupForm()
		else:
			info['groups'] = request.user.groups.all()

	return render(request, 'groups.html', info)

def groupinfo(request, groupname):
	if request.method == "POST" and request.user.is_superuser:
		group = Group.objects.get(name=groupname)
		newmember = User.objects.get(username=request.POST['username'])
		newmember.groups.add(group)
		return HttpResponseRedirect(groupname)
	else:
		namedgroup = request.user.groups.filter(name=groupname)
		if namedgroup.exists() or request.user.is_superuser:
			info = {}
			info['admin'] = request.user.is_superuser
			info['form'] = UserForm
			info['groupusers'] = User.objects.filter(groups__name=groupname)
			return render(request, 'groupinfo.html', info)
		else:
			return HttpResponseForbidden("forbidden")