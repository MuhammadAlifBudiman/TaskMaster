from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django import forms
from django.http import JsonResponse
import json
from .models import *

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegisterForm(UserCreationForm):
    fullname = forms.CharField(max_length=255, label='fullname', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-style"})

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        if not fullname.isalpha():
            raise forms.ValidationError("Full name should only contain alphabetic characters.")
        return fullname

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'fullname']

def index(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    completed_daily_tasks = Task.objects.filter(completed=True, daily=True, user=request.user).count()
    total_daily_tasks = Task.objects.filter(daily=True, user=request.user).count()
    remaining_daily_tasks = total_daily_tasks - completed_daily_tasks
    completed_weekly_tasks = Task.objects.filter(completed=True, weekly=True, user=request.user).count()
    total_weekly_tasks = Task.objects.filter(weekly=True, user=request.user).count()
    remaining_weekly_tasks = total_weekly_tasks - completed_weekly_tasks
    completed_all_tasks = (completed_daily_tasks+completed_weekly_tasks) == (total_daily_tasks+total_weekly_tasks) and (total_daily_tasks+total_weekly_tasks) != 0

    return render(request, 'taskmaster/index.html', 
            {
                'completed_daily_tasks': completed_daily_tasks, 
                'total_daily_tasks': total_daily_tasks,
                'remaining_daily_tasks': remaining_daily_tasks,
                'completed_weekly_tasks': completed_weekly_tasks,
                'total_weekly_tasks': total_weekly_tasks,
                'remaining_weekly_tasks': remaining_weekly_tasks,
                'completed_all_tasks': completed_all_tasks
            })

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    login_form = UserLoginForm()
    register_form = UserRegisterForm()
    return render(request, 'taskmaster/auth.html', {'login_form': login_form, 'register_form': register_form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        login_form = UserLoginForm(data=request.POST)
        register_form = UserRegisterForm()
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f'Logged in successfully.')
            return redirect('index')
        elif not login_form.has_error('username') and not login_form.has_error('password'):
            messages.error(request, f'Invalid username or password.')
            return render(request, 'taskmaster/auth.html', {'login_form': login_form, 'register_form': register_form})
        else:    
            return render(request, 'taskmaster/auth.html', {'login_form': login_form, 'register_form': register_form})
    else:
        login_form = UserLoginForm()
        register_form = UserRegisterForm()

    return render(request, 'taskmaster/auth.html', {'login_form': login_form, 'register_form': register_form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    checked = True
    if request.method == 'POST':
        login_form = UserLoginForm()
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            userprofile = UserProfile.objects.create(user=user)
            userprofile.save()
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
        elif register_form.has_error('password2'):
            register_form.fields['password1'].widget.attrs['class'] = 'is-invalid'
        else:
            messages.error(request, f'An error occurred. Please try again later.')

    else:
        login_form = UserLoginForm()
        register_form = UserRegisterForm()

    return render(request, 'taskmaster/auth.html', {'login_form': login_form, 'register_form': register_form, 'checked': checked})



def logout_view(request):
    logout(request)
    messages.success(request, f'Logged out successfully.')
    return redirect('auth')


def dailytask(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    tasks = Task.objects.filter(daily=True, user=request.user).order_by('created_at')  # Fetching daily tasks from the database
    completed_tasks = tasks.filter(completed=True).count()
    total_tasks = tasks.count()

    return render(request, 'taskmaster/dailytask.html', {'tasks':tasks, 'completed_tasks': completed_tasks, 'total_tasks': total_tasks})


def weeklytask(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    tasks = Task.objects.filter(weekly=True, user=request.user).order_by('created_at')  # Fetching weekly tasks from the database
    completed_tasks = tasks.filter(completed=True).count()
    total_tasks = tasks.count()

    return render(request, 'taskmaster/weeklytask.html', {'tasks':tasks, 'completed_tasks': completed_tasks, 'total_tasks': total_tasks})


def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        recurrent = request.POST.get('recurrent')
        daily = False
        weekly = False
        if recurrent == "daily":
            execution_time = request.POST.get('executiontime')
            daily = True
            task = Task(user=request.user, title=title, description=description, execution_time=execution_time, daily=daily, weekly=weekly)
            task.save()
            return redirect('dailytask')
        elif recurrent == "weekly":
            execution_time = request.POST.get('execution_time')
            execution_day = request.POST.get('execution_day')
            weekly = True
            task = Task(user=request.user, title=title, description=description, execution_time=execution_time,execution_day=execution_day, daily=daily, weekly=weekly)
            task.save()
            return redirect('weeklytask')

    return redirect('index')


def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        task.title = title
        task.description = description

        if task.daily:
            execution_time = request.POST.get('executiontime')
            task.execution_time = execution_time
            task.save()
            return redirect('dailytask')
        else:
            execution_time = request.POST.get('execution_time')
            execution_day = request.POST.get('execution_day')
            task.execution_time = execution_time
            task.execution_day = execution_day
            task.save()
            return redirect('weeklytask')

    return redirect('index')


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        if task.daily:
            return redirect('dailytask')
        else:
            return redirect('weeklytask')
    
    return redirect('index')


def mark_task_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        if task.daily:
            return redirect('dailytask')
        else:
            return redirect('weeklytask')

    return redirect('index')


def set_timezone(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)

        # Extract the timeZone value from the JSON data
        time_zone = data.get('timeZone')
        # Get the user's profile or create it if it doesn't exist
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if created:
            profile = profile[0]  # Access the created profile from the tuple
        profile.timezone = time_zone
        profile.save()

        # Set the time zone for the current request
        timezone.activate(time_zone)
        return JsonResponse({'success': True})


def check_username_availability(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        response_data = {'is_available': not User.objects.filter(username=username).exists()}
        return JsonResponse(response_data)
    return JsonResponse({'is_available': False})