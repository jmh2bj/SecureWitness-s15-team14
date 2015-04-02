from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Permission, Group

class Report(models.Model):
	rep_title = models.CharField(max_length=200)
	rep_created = models.DateTimeField('date created')
	short_desc = models.CharField(max_length=200)
	detailed_desc = models.CharField(max_length=2000)
	loc = models.CharField(max_length=200)
	rep_date = models.DateTimeField('report date')
	keywords = models.CharField(max_length=500)
	file = models.FileField(upload_to='reports', blank=True)
	isPublic = models.BooleanField(default=True)
	allowed_users = models.ForeignKey(User) #individual users granted access to a report
	allowed_groups = models.ForeignKey(Group) #groups whose members are granted access to a report

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
