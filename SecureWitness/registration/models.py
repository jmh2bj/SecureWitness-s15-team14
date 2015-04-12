from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Permission, Group

class Report(models.Model):
	rep_title = models.CharField(max_length=200)
	rep_created = models.DateTimeField('date created', auto_now_add=True)
	short_desc = models.CharField(max_length=200)
	detailed_desc = models.CharField(max_length=2000)
	# location should be a reference to the folders, probably
	#loc = models.CharField(max_length=200)
	rep_date = models.DateTimeField('report date')
	keywords = models.CharField(max_length=500)
	file = models.FileField(upload_to='reports', blank=True, null=True)
	isPublic = models.BooleanField(default=True)
	allowed_users = models.ManyToManyField(User, related_name="allowed_users", null=True, blank=True) #individual users granted access to a report
	allowed_groups = models.ManyToManyField(Group, null=True, blank=True) #groups whose members are granted access to a report
	owner = models.ForeignKey(User, null=True)

	def __str__(self):
		return self.rep_title

class Folder(models.Model):
	name = models.CharField(max_length=200)
	owner = models.ForeignKey(User, null=True)
	contained_folders = models.ManyToManyField(Folder, null=True, blank=True)
	contained_reports = models.ManyToManyField(Report, null=True, blank=True)

	def __str__(self):
		return self.name

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
		fields = ('rep_title', 'short_desc', 'detailed_desc', 'rep_date', 'keywords', 'file', 'isPublic', 'allowed_users', 'allowed_groups')