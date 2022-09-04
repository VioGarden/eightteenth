from django import forms
from django.forms import ModelForm
from .models import MySongUser

class MySongUserForm(ModelForm):
    class Meta:
        model = MySongUser
        fields = ('MyUser',)
