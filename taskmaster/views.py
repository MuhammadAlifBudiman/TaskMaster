from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from .forms.forms import *
import json
from .models import *
from rest_framework import viewsets, status
from .serializers.serializers import *

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        user_id = self.request.query_params.get('user_id')
        daily = self.request.query_params.get('daily')
        weekly = self.request.query_params.get('weekly')
        monthly = self.request.query_params.get('monthly')
        completed = self.request.query_params.get('completed')
        days = self.request.query_params.get('days')
        date = self.request.query_params.get('days')

        if user_id:
            queryset = queryset.filter(user=user_id)
        if daily == 'true':
            queryset = queryset.filter(daily=True)
        if weekly == 'true':
            queryset = queryset.filter(weekly=True)
        if monthly == 'true':
            queryset = queryset.filter(monthly=True)
        if completed == 'true':
            queryset = queryset.filter(completed=True)
        if days:
            queryset = queryset.filter(execution_day=days.capitalize())
        if date:
            queryset = queryset.filter(execution_date=date)

        return queryset


def index(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    completed_daily_tasks = Task.objects.filter(completed=True, daily=True, user=request.user).count()
    total_daily_tasks = Task.objects.filter(daily=True, user=request.user).count()
    remaining_daily_tasks = total_daily_tasks - completed_daily_tasks

    completed_weekly_tasks = Task.objects.filter(completed=True, weekly=True, user=request.user).count()
    total_weekly_tasks = Task.objects.filter(weekly=True, user=request.user).count()
    remaining_weekly_tasks = total_weekly_tasks - completed_weekly_tasks

    completed_monthly_tasks = Task.objects.filter(completed=True, monthly=True, user=request.user).count()
    total_monthly_tasks = Task.objects.filter(monthly=True, user=request.user).count()
    remaining_monthly_tasks = total_monthly_tasks - completed_monthly_tasks

    completed_all_tasks = (completed_daily_tasks+completed_weekly_tasks) == (total_daily_tasks+total_weekly_tasks) and (total_daily_tasks+total_weekly_tasks) != 0

    return render(request, 'taskmaster/index.html', 
            {
                'completed_daily_tasks': completed_daily_tasks, 
                'total_daily_tasks': total_daily_tasks,
                'remaining_daily_tasks': remaining_daily_tasks,
                'completed_weekly_tasks': completed_weekly_tasks,
                'total_weekly_tasks': total_weekly_tasks,
                'remaining_weekly_tasks': remaining_weekly_tasks,
                'completed_monthly_tasks': completed_monthly_tasks,
                'total_monthly_tasks': total_monthly_tasks,
                'remaining_monthly_tasks': remaining_monthly_tasks,
                'completed_all_tasks': completed_all_tasks,

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

    form = TaskForm()
    tasks = Task.objects.filter(daily=True, user=request.user).order_by('created_at')  # Fetching daily tasks from the database
    completed_tasks = tasks.filter(completed=True).count()
    total_tasks = tasks.count()

    return render(request, 'taskmaster/dailytask.html', {'tasks':tasks, 'completed_tasks': completed_tasks, 'total_tasks': total_tasks, 'form':form})


def weeklytask(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    form = TaskForm()
    tasks = Task.objects.filter(weekly=True, user=request.user).order_by('created_at')  # Fetching weekly tasks from the database
    completed_tasks = tasks.filter(completed=True).count()
    total_tasks = tasks.count()
    
    return render(request, 'taskmaster/weeklytask.html', {'tasks':tasks, 'completed_tasks': completed_tasks, 'total_tasks': total_tasks, 'form':form})


def monthlytask(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    form = TaskForm()
    tasks = Task.objects.filter(monthly=True, user=request.user).order_by('created_at')  # Fetching monthly tasks from the database
    completed_tasks = tasks.filter(completed=True).count()
    total_tasks = tasks.count()
    
    return render(request, 'taskmaster/monthlytask.html', {'tasks':tasks, 'completed_tasks': completed_tasks, 'total_tasks': total_tasks, 'form':form})


def add_task(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'task <b>{task.title}</b> has been added')
            if task.daily:
                return redirect('dailytask')
            elif task.weekly:
                return redirect('weeklytask')
            elif task.monthly:
                return redirect('monthlytask')


        else:
            messages.error(request, "An error occurred. Please try again")
            if form.cleaned_data.get('daily'):
                return redirect('dailytask')
            elif form.cleaned_data.get('weekly'):
                return redirect('weeklytask')
            elif form.cleaned_data.get('monthly'):
                return redirect('monthlytask')
            else:
                return redirect('index')

     


def edit_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id, user=request.user)
        form = TaskForm(request.POST)
        if form.is_valid():
            form = TaskForm(request.POST, instance=task)
            task = form.save()
            messages.success(request, f'Task <b>{task.title}</b> has been edited')
            if task.daily:
                return redirect('dailytask')
            elif task.weekly:
                return redirect('weeklytask')
            elif task.monthly:
                return redirect('monthlytask')

        else:
            messages.error(request, f'An error occurred. Please try again.')
            if form.cleaned_data.get('daily'):
                return redirect('dailytask')
            elif form.cleaned_data.get('weekly'):
                return redirect('weeklytask')
            elif form.cleaned_data.get('monthly'):
                return redirect('monthlytask')
            else:
                return redirect('index')



def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        if task:
            messages.success(request, f'task <b>{task.title}</b> has been deleted')

        if task.daily:
            return redirect('dailytask')
        elif task.weekly:
            return redirect('weeklytask')
        elif task.monthly:
            return redirect('monthlytask')

    


def mark_task_complete(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
        if(task.completed):
            messages.success(request, f'task {task.title}</b> has been completed')

        if task.daily:
            return redirect('dailytask')
        elif task.weekly:
            return redirect('weeklytask')
        elif task.monthly:
            return redirect('monthlytask')


    


#API

def set_timezone(request):
    """
    docstirng for documentations
    """
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


