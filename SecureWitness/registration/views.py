import tkinter
from coverage import data
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import Permission, User, Group
from registration.models import UserForm, GroupForm, ReportForm, Report, FolderForm, Folder
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

def home(request):
	return add_user(request)

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
	
	return render(request, 'registration/confirm.html', {'permissions': permissions, 'user': request.user})

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
	if report.owner == request.user:
		info['form'] = ReportForm(instance=report)
		info['pk'] = pk
	else:
		return HttpResponseForbidden("forbidden")
	if request.method == "POST" and request.user.is_authenticated() and report.owner == request.user:
		if 'update_report' in request.POST:
			report_form = ReportForm(request.POST)
			if report_form.is_valid():
				report_form=ReportForm(request.POST, instance = report)
				report_form.save()	
			info['form'] = report_form
		elif 'copy_report' in request.POST:
			info['form'] = ReportForm(request.POST)
			newReport = Report.objects.create(owner=request.user, rep_title=request.POST['rep_title'], short_desc=request.POST['short_desc'], detailed_desc=request.POST['detailed_desc'], rep_date=request.POST['rep_date'], keywords=request.POST['keywords'], isPublic=request.POST['isPublic'])
			if 'file' in request.POST:
				newReport.file = request.POST['file']
			if 'allowed_groups' in request.POST:
				newReport.allowed_groups = request.POST['allowed_groups']
			if 'allowed_users' in request.POST:
				newReport.allowed_users = request.POST['allowed_users']

	return render(request, 'reportinfo.html', info)

def deletereport(request, pk):
	report = Report.objects.filter(pk=pk)
	if report[0].owner == request.user:
		report.delete()
	return HttpResponseRedirect('/reports/')

def deletefolder(request, pk):
	folder = Folder.objects.filter(pk=pk)
	if folder[0].owner == request.user:
		folder.delete()
	return HttpResponseRedirect('/folders/')

def folders(request):
	info = {}
	if request.method == "POST" and request.user.is_authenticated():
		newFolder = Folder.objects.create(owner=request.user, name=request.POST['name'])
	else:
		info['form'] = FolderForm()
	if not request.user.is_authenticated():
		info['folders'] = ["no user logged in"]
		info['user'] = False
	else:
		info['user'] = True
		info['folders'] = Folder.objects.filter(owner=request.user)

	return render(request, 'folders.html', info)

def folderinfo(request, pk):
	folder = get_object_or_404(Folder, pk=pk)
	info = {}
	if folder.owner == request.user:
		info['form'] = FolderForm(instance = folder)
		info['folders'] = folder.contained_folders.all()
		info['reports'] = folder.contained_reports.all()
		info['pk'] = pk
	else:
		return HttpResponseForbidden("forbidden")
	if request.method == "POST" and request.user.is_authenticated() and folder.owner == request.user:
		folder_form = FolderForm(request.POST)
		folder.name = request.POST['name']
		folder.save()
		if 'folderadd' in request.POST:
			folderadd = Folder.objects.filter(name=request.POST['folderadd'], owner=request.user)
			if len(folderadd) > 0: 
				folder.contained_folders.add(folderadd[0])
		if 'reportadd' in request.POST:
			reportadd = Report.objects.filter(rep_title=request.POST['reportadd'], owner=request.user)
			if len(reportadd) > 0: 
				folder.contained_reports.add(reportadd[0])
		info['form'] = folder_form
	return render(request, 'folderinfo.html', info)

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

def searchform(request):
    user = request.GET.get("type")
    report = request.POST.get("type2")
    q = request.GET.get("q")
    title = request.GET.get("type3")
    shortd = request.GET.get("type4")
    detaild = request.GET.get("type5")
    repd = request.GET.get("type6")
    key = request.GET.get("type7")
    file = request.GET.get("type8")
    results = ""
    if title:
        if q:
            results = Report.objects.filter(rep_title__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "searchform.html", context)
    elif shortd:
        if q:
            results = Report.objects.filter(short_desc__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "searchform.html", context)
    elif detaild:
        if q:
            results = Report.objects.filter(detailed_desc__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "searchform.html", context)
    elif repd:
        if q:
            results = Report.objects.filter(rep_date__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "searchform.html", context)
    elif key:
        if q:
            results = Report.objects.filter(keywords__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "searchform.html", context)
    elif file:
        if q:
            results = Report.objects.filter(file__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "searchform.html", context)
    elif user:
        if q:
        # you may want to use `__istartswith' instead
            results = User.objects.filter(username__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "searchform.html", context)
    else:
        results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "searchform.html", context)



def search(request):
    user = request.GET.get("type")
    report = request.GET.get("type2")
    q = request.GET.get("q")
    title = request.GET.get("type3")
    shortd = request.GET.get("type4")
    detaild = request.GET.get("type5")
    repd = request.GET.get("type6")
    key = request.GET.get("type7")
    file = request.GET.get("type8")
    results = ""
    if title:
        if q:
            results = Report.objects.filter(rep_title__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "search.html", context)
    elif shortd:
        if q:
            results = Report.objects.filter(short_desc__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "search.html", context)
    elif detaild:
        if q:
            results = Report.objects.filter(detailed_desc__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "search.html", context)
    elif repd:
        if q:
            results = Report.objects.filter(rep_date__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "search.html", context)
    elif key:
        if q:
            results = Report.objects.filter(keywords__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "search.html", context)
    elif file:
        if q:
            results = Report.objects.filter(file__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "search.html", context)
    elif user:
        if q:
        # you may want to use `__istartswith' instead
            results = User.objects.filter(username__icontains=q)
        else:
        # you may want to return Customer.objects.none() instead
            results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "search.html", context)
    else:
        results = User.objects.none()
        context = dict(results=results, q=q)
        return render(request, "search.html", context)
