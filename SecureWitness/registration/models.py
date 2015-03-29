from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserForm(ModelForm):
	class Meta:
		password = forms.CharField(widget=forms.PasswordInput)
		model = User
		widgets = {
			'password': forms.PasswordInput(),
		}
		fields = ('username', 'email', 'password')