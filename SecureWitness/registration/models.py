from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Permission, Group

class Report(models.Model):
	rep_title = models.CharField("Report Title", max_length=200)
	rep_created = models.DateTimeField('date created', auto_now_add=True)
	short_desc = models.CharField("Short Description", max_length=200)
	detailed_desc = models.CharField("Detailed Description", max_length=2000)
	loc = models.CharField("Location", max_length=200, blank=True)
	rep_date = models.DateTimeField('Report date', blank=True)
	keywords = models.CharField("Associated Keywords", max_length=500, blank=True)
	rep_file = models.FileField(upload_to='reports', blank=True, null=True)
	isPublic = models.BooleanField("Public Report?" , default=True)
	allowed_users = models.ManyToManyField(User, related_name="allowed_users", null=True, blank=True, verbose_name="Allowed Users") #individual users granted access to a report
	allowed_groups = models.ManyToManyField(Group, null=True, blank=True, verbose_name="Allowed Groups") #groups whose members are granted access to a report
	owner = models.ForeignKey(User, null=True)

	def __str__(self):
		return self.rep_title

class Folder(models.Model):
	name = models.CharField(max_length=200)
	owner = models.ForeignKey(User, null=True)
	contained_folders = models.ManyToManyField("self", symmetrical=False, null=True)
	contained_reports = models.ManyToManyField(Report, null=True, blank=True)

	def __str__(self):
		return self.name

class UserRoles(models.Model):
	class Meta:
		permissions = [
            ("admin", "Is a SecureWitness Admin")
        ]

class FolderForm(ModelForm):
	folderadd = forms.CharField(max_length=200, required=False)
	reportadd = forms.CharField(max_length=200, required=False)
	class Meta:
		model = Folder
		fields = ('name',)

#class ReportFile(models.Model):
#	report = models.ForeignKey(Report)
#	rep_file = models.FileField(upload_to='reports', blank=True, null=True)
#	isEncrypted = models.BooleanField(default=False)

class UserForm(ModelForm):
	class Meta:
		password = forms.CharField(widget=forms.PasswordInput)
		model = User
		widgets = {
			'password': forms.PasswordInput(),
		}
		fields = ('username', 'email', 'password')

class GroupForm(ModelForm):
	class Meta:
		model = Group
		fields = ('name',)

class ReportForm(ModelForm):
	class Meta:
		model = Report
		fields = ('rep_title', 'short_desc', 'detailed_desc', 'loc', 'rep_date', 'keywords','rep_file', 'isPublic', 'allowed_users', 'allowed_groups')