from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'taskmaster/index.html')

def login_view(request):
    return render(request, 'taskmaster/login.html')

def register_view(request):
    return render(request, 'taskmaster/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')
