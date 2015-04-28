import os
from django.core.files.base import ContentFile
from itertools import chain
from coverage import data
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import Permission, User, Group
from registration.models import UserForm, GroupForm, ReportForm, Report, FolderForm, Folder, PermissionForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from crypt.py import create_private_key, en_crypt, make_key
import os

def userAllowed(user, report):
	if report.isPublic: return True
	elif report.allowed_users.filter(username=user.username).exists(): return True
	elif report.owner == user: return True
	for i in report.allowed_groups.all():
		if user.groups.filter(name=i.name).exists(): return True
	return False

def popular(request):
	info = {}
	reports = Report.objects.filter(isPublic=True)
	info['viewedreports'] = reports.order_by('views').reverse()[:5]
	info['likedreports'] = sorted(list(reports), key=lambda x: x.upvotecount)
	info['likedreports'].reverse()
	info['likedreports'] = info['likedreports'][:5]
	return render(request, 'popular.html', info)

def upvote(request, pk):
	report = get_object_or_404(Report, pk=pk)
	if userAllowed(request.user, report) and not report.upvotes.filter(username=request.user.username): #if user is allowed to see report and hasn't already voted
		report.upvotes.add(request.user)
		report.downvotes.remove(request.user)
	return HttpResponseRedirect('/reports/' + pk)

def downvote(request, pk):
	report = get_object_or_404(Report, pk=pk)
	if userAllowed(request.user, report) and not report.downvotes.filter(username=request.user.username): #if user is allowed to see report and hasn't already voted
		report.downvotes.add(request.user)
		report.upvotes.remove(request.user)
	return HttpResponseRedirect('/reports/' + pk)

def home(request):
	return HttpResponseRedirect('/registration/create')

def add_user(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			users = User.objects.all()
			if not users.exists():
				admin = Permission.objects.get(codename='admin')
				newUser = User.objects.create_user(**form.cleaned_data)
				newUser.user_permissions = [admin]
			else:
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
				return HttpResponse("logged in")
				#return HttpResponseRedirect('confirm')
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
	info = {}
	info['user'] = request.user
	if not request.user.is_authenticated():
		info['permissions'] = "no user logged in"
	else:
		info['admin'] = request.user.has_perm('registration.admin')
		info['permissions'] = str(request.user.get_all_permissions())
	
	return render(request, 'registration/confirm.html', info)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('login')

def users(request):
	if request.user.is_authenticated() and request.user.has_perm('registration.admin'):
		info = {}
		info['users'] = User.objects.all()
		return render(request, 'registration/users.html', info)
	else:
		return HttpResponseForbidden('forbidden')

def userinfo(request, pk):
	if request.user.is_authenticated() and request.user.has_perm('registration.admin'):
		info = {}
		info['user'] = get_object_or_404(User, pk=pk)
		if request.method == "POST":
			if 'admin' in request.POST and not info['user'].has_perm('registration.admin') and request.POST['admin']:
				admin = Permission.objects.get(codename='admin')
				info['user'].user_permissions = [admin]
			elif not 'admin' in request.POST and info['user'].has_perm('registration.admin'):
				info['user'].user_permissions = []
			if 'active' in request.POST and not info['user'].is_active and request.POST['active']:
				info['user'].is_active = request.POST['active']
			elif not 'active' in request.POST and info['user'].is_active:
				info['user'].is_active = False
			info['user'].save()
			return HttpResponseRedirect(str(pk))
			#return HttpResponse(str(request.POST['active']) + str(request.POST['admin']))
		initial = {}
		initial['active'] = info['user'].is_active
		initial['admin'] = info['user'].has_perm('registration.admin')
		info['form'] = PermissionForm(initial=initial)
		return render(request, 'registration/userinfo.html', info)
	else:
		return HttpResponseForbidden('forbidden')

def reports(request):
	info = {}
	if request.method == "POST" and request.user.is_authenticated():
		info['form'] = ReportForm(request.POST, request.FILES)
		newReport = Report.objects.create(owner=request.user, rep_title=request.POST['rep_title'], short_desc=request.POST['short_desc'], detailed_desc=request.POST['detailed_desc'])
		if 'rep_file' in request.FILES:
			f = request.FILES.get('rep_file')
			newReport.rep_file = f
		if 'loc' in request.POST:
			newReport.loc = request.POST['loc']
		if 'rep_date' in request.POST:
			newReport.rep_date = request.POST['rep_date']
		if 'keywords' in request.POST:
			newReport.keywords = request.POST['keywords']
		if 'isPublic' in request.POST and request.POST['isPublic']:
			newReport.isPublic = True
		else:
			newReport.isPublic = False
		if 'allowed_groups' in request.POST:
			newReport.allowed_groups = request.POST['allowed_groups']
		if 'allowed_users' in request.POST:
			newReport.allowed_users = request.POST['allowed_users']
		newReport.save()
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
	if userAllowed(request.user, report): #check for whenever a user can see it, including if they're allowed, or if they're in a group that's allowed
		info['form'] = ReportForm(instance=report)
		info['pk'] = pk
		report.views = report.views + 1
		report.save()
	else:
		return HttpResponseForbidden("forbidden")
	if request.method == "POST" and request.user.is_authenticated() and report.owner == request.user:
		if 'update_report' in request.POST:
			report_form = ReportForm(request.POST, request.FILES)
			if report_form.is_valid():
				report_form=ReportForm(request.POST, request.FILES, instance = report)
				if 'rep_file' in request.FILES:
					f = request.FILES.get('rep_file')
					report_form.rep_file = f
					Report.objects.filter(pk=pk).update(rep_file=f)
					#return HttpResponse(report_form.rep_file)
				report_form.save()
			info['form'] = report_form
		elif 'copy_report' in request.POST:
			info['form'] = ReportForm(request.POST, request.FILES)
			newReport = Report.objects.create(owner=request.user, rep_title=request.POST['rep_title'], short_desc=request.POST['short_desc'], detailed_desc=request.POST['detailed_desc'], isPublic=request.POST['isPublic'])
			if 'rep_file' in request.FILES:
				f = request.FILES.get('rep_file')
				newReport.rep_file = f
			if 'loc' in request.POST:
				newReport.loc = request.POST['loc']
			if 'rep_date' in request.POST:
				newReport.rep_date = request.POST['rep_date']
			if 'keywords' in request.POST:
				newReport.keywords = request.POST['keywords']
			if 'allowed_groups' in request.POST:
				newReport.allowed_groups = request.POST['allowed_groups']
			if 'allowed_users' in request.POST:
				newReport.allowed_users = request.POST['allowed_users']
			newReport.save()
		elif 'encrypt_file' in request.POST:
			report_form = ReportForm(request.POST, request.FILES)
			if 'rep_file' in request.FILES:
				f = request.FILES.get('rep_file')
				key_file = f.name + "_key"
				encfile = f.name + "_enc"
				key = create_private_key()
				path_enc = os.path.join(settings.MEDIA_ROOT, 'reports', encfile)
				path_file = os.path.join(settings.MEDIA_ROOT, 'reports', f.name)
				path_key = os.path.join(settings.MEDIA_ROOT, 'reports', key_file)
				en_crypt(path_key, path_enc, path_file)
				f_enc = open(path_enc, "w+b")
				report_form.rep_file = f_enc
				Report.objects.filter(pk=pk).update(rep_file=f_enc)
				if report_form.is_valid():
					report_form.save()
					return HttpResponse("File Encrypted and uploaded")
				else:
					return HttpResponse("Form is not valid")

					
			else:
				return HttpResponse("No file to encrypt.")

	return render(request, 'reportinfo.html', info)

def download(request, filename):
	path_to_file = os.path.realpath('reports/' + filename)
	f = open(path_to_file, 'r')
	myfile = f.read()
	response = HttpResponse(myfile, content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response


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
	if request.method == "POST" and request.user.has_perm('registration.admin'):
		Group.objects.create(name=request.POST['name'])
	info = {}
	if not request.user.is_authenticated():
		info['groups'] = ["no user logged in"]
	else:
		if request.user.has_perm('registration.admin'):
			info['admin'] = True
			info['groups'] = Group.objects.all()
			info['form'] = GroupForm()
		else:
			info['groups'] = request.user.groups.all()

	return render(request, 'groups.html', info)

def groupinfo(request, groupname):
	if request.method == "POST" and request.user.has_perm('registration.admin'):
		group = Group.objects.get(name=groupname)
		newmember = User.objects.get(username=request.POST['username'])
		newmember.groups.add(group)
		return HttpResponseRedirect(groupname)
	else:
		namedgroup = request.user.groups.filter(name=groupname)
		if namedgroup.exists() or request.user.has_perm('registration.admin'):
			info = {}
			info['admin'] = request.user.has_perm('registration.admin')
			info['form'] = UserForm
			info['groupusers'] = User.objects.filter(groups__name=groupname)
			return render(request, 'groupinfo.html', info)
		else:
			return HttpResponseForbidden("forbidden")

def searchform(request):
    errors = []
    user = request.GET.get("type")
    q = request.GET.get("q")
    title = request.GET.get("type3")
    shortd = request.GET.get("type4")
    detaild = request.GET.get("type5")
    repd = request.GET.get("type6")
    key = request.GET.get("type7")
    file = request.GET.get("type8")
    allr = request.GET.get("type9")

    results = ""
    result = ""
    results1 = ""
    results2 = ""

    if not (title or shortd or detaild or repd or key or file or user or allr):
        errors.append('Please Enter a Search Term')
    elif (title or shortd or detaild or repd or key or file):
        result = Report.objects.filter(rep_title__icontains=title).filter(short_desc__icontains=shortd).\
            filter(detailed_desc__icontains=detaild).filter(rep_date__icontains=repd).\
            filter(keywords__icontains=key).filter(rep_file__icontains=file)
        results1 = result.filter(isPublic=True)
        results2 = result.filter(isPublic=False)
        results3 = results2.filter(allowed_users=request.user).filter(owner=request.user)
        results4 = [r for r in request.user.groups.all() if r in results2.allowed_users.all()]
        results = list(chain(results1, results3, results4))
        context = dict(results=results, q=title)
        return render(request, "searchform.html", context)
    elif user:
        results = User.objects.filter(username__icontains=user)
        context = dict(results=results, q=user)
        return render(request, "searchform.html", context)
    elif allr:
        #reports = Report.objects.get()
        #context = {'reports': reports}
        results = Report.objects.filter(isPublic=True)
        context = dict(results=results, q=results)
        return render(request, "searchform.html", context)
    return render(request, "searchform.html")

def visiblereports(request):
    result = Report.objects.filter(isPublic=True)
    result1 = Report.objects.filter(isPublic=False)
    results3 = result1.filter(allowed_users=request.user)
    results4 = result1.filter(owner=request.user)
    results5 = result1.filter(allowed_groups = request.user.groups.all())
    results = list(chain(result, results3, results4, results5))
    context = dict(results=results, allr=True)
    return render(request, "visiblereports.html", context)

def search(request):
    errors = []
    user = request.GET.get("type")
    q = request.GET.get("q")
    title = request.GET.get("type3")
    shortd = request.GET.get("type4")
    detaild = request.GET.get("type5")
    repd = request.GET.get("type6")
    key = request.GET.get("type7")
    file = request.GET.get("type8")
    allr = request.GET.get("type9")
    loc = request.GET.get("type10")
    results = ""
    result = ""
    results1 = ""
    results2 = ""
    result1 = ""
    if not (title or shortd or detaild or repd or key or file or user or allr or loc):
        errors.append('Please Enter a Search Term')
    elif (title or shortd or detaild or repd or key or file or loc):
        result = Report.objects.filter(rep_title__icontains=title).filter(short_desc__icontains=shortd).\
            filter(detailed_desc__icontains=detaild).filter(rep_date__icontains=repd).\
            filter(keywords__icontains=key).filter(rep_file__icontains=file).filter(loc__icontains=loc)
        results1 = result.filter(isPublic=True)
        results2 = result.filter(isPublic=False)
        results3 = results2.filter(allowed_users=request.user)
        results4 = results2.filter(owner=request.user)
        results5 = results2.filter(allowed_groups = request.user.groups.all())
        results = list(chain(results1, results3, results4, results5))
        context = dict(results=results, title=True, shortd=True, detaild=True, repd=True,
                       key=True, file=True, loc=True)
        return render(request, "search.html", context)
    elif user:
        results = User.objects.filter(username__icontains=user)
        context = dict(results=results, q=user)
        return render(request, "search.html", context)
    elif allr:
        #reports = Report.objects.get()
        #context = {'reports': reports}
        result = Report.objects.filter(isPublic=True)
        result1 = Report.objects.filter(isPublic=False)
        results3 = result1.filter(allowed_users=request.user)
        results4 = result1.filter(owner=request.user)
        results5 = result1.filter(allowed_groups = request.user.groups.all())
        results = list(chain(result, results3, results4, results5))
        context = dict(results=results, allr=True)
        return render(request, "search.html", context)
    return render(request, "search.html")
