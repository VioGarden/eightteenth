from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(
        required=False, 
        widget=forms.EmailInput(
        attrs={'class':'register-form', 'placeholder': 'email (optional)'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'register-form'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].help_text = 'Letters, digits and @/./+/-/_ only'
        self.fields['password1'].widget.attrs['class'] = 'register-form'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        # self.fields['password1'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'register-form'
        self.fields['password2'].widget.attrs['placeholder'] = 'password (confirm)'
        # self.fields['password2'].help_text = ''