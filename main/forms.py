from django import forms
from django.forms import ModelForm

from .models import *


class TaskForm(forms.ModelForm):
	tasktitle= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Add new task...'}))

	class Meta:
		model = Tasks
		fields = '__all__'