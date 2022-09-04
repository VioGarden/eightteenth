from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from search.forms import MySongUserForm
from search.models import *

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        mysonguser = authenticate(request, username=username, password=password)
        if mysonguser is not None:
            login(request, mysonguser)
            return redirect('home')
        else:
            messages.success(request, ("Error Logging In, Try Again"))
            return redirect('login-user')
    else:
        return render(request, 'authentication/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)  #if user fills out form, pass
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            form_register = MySongUserForm()
            x = form_register.save(commit=False)
            x.MyUser = user
            x.save()
            messages.success(request, ("Registration Successful!"))
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authentication/register_user.html', {
        "form": form
    })

