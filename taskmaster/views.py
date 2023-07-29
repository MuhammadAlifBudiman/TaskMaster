from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from .forms.forms import *
from .models import *
from .serializers.serializers import *


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

    completed_all_tasks = (completed_daily_tasks+completed_weekly_tasks+completed_monthly_tasks) == (total_daily_tasks+total_weekly_tasks+total_monthly_tasks) and (total_daily_tasks+total_weekly_tasks+total_monthly_tasks) != 0

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


def export_task_to_excel(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    # Create a new Excel workbook
    workbook = Workbook()

    # Write headers for each table section
    task_types = ["Daily", "Weekly", "Monthly"]

    # Function to write section header
    def write_section_header(section_name):
        nonlocal row_index
        sheet.merge_cells(start_row=row_index, start_column=1, end_row=row_index, end_column=len(headers))
        merged_cell = sheet.cell(row=row_index, column=1, value=section_name)
        merged_cell.font = Font(bold=True)
        merged_cell.alignment = Alignment(horizontal='center')
        merged_cell.fill = PatternFill(start_color='999999', end_color='999999', fill_type='solid')

        for col_index, header in enumerate(headers, start=1):
            sheet.cell(row=row_index + 1, column=col_index, value=header).font = Font(bold=True)
            sheet.cell(row=row_index + 1, column=col_index).alignment = Alignment(horizontal='center')
            sheet.cell(row=row_index + 1, column=col_index).fill = PatternFill(start_color='C0C0C0', end_color='C0C0C0', fill_type='solid')
            col_letter = get_column_letter(col_index)
            column_width = len(header) + 2  # Adjust width based on header length
            sheet.column_dimensions[col_letter].width = column_width
        row_index += 2

    
    for task_type in task_types:
        # Create a new sheet for each task type
        sheet = workbook.create_sheet(title=task_type)

        # Write headers for each table section
        headers = ["Date", "Title", "Description", "Execution_time", "Completed"]

        row_index = 1

        write_section_header(task_type)

        # Fetch and populate tasks for each type
        tasks = TaskHistory.objects.filter(task_type=task_type.lower(), user=request.user)
        for task in tasks:
            execution_time = task.execution_time.strftime('%H:%M')
            if task.task_type == 'daily':
                data = [task.date.strftime('%d-%m-%Y'), task.title, task.description, execution_time, 'yes' if task.completed else 'no']
            elif task.task_type == 'weekly':
                data = [task.date.strftime('%d-%m-%Y'), task.title, task.description, f'{task.execution_day}, {execution_time}', 'yes' if task.completed else 'no']
            else:
                data = [task.date.strftime('%d-%m-%Y'), task.title, task.description, f'Day {task.execution_date}, {execution_time}', 'yes' if task.completed else 'no']

            for col_index, value in enumerate(data, start=1):
                sheet.cell(row=row_index, column=col_index, value=value)
                col_letter = get_column_letter(col_index)
                column_width = len(str(value)) + 2  # Adjust width based on content length
                if sheet.column_dimensions[col_letter].width < column_width:
                    sheet.column_dimensions[col_letter].width = column_width if column_width < 30 else 30
            row_index += 1

        # Add a border to the table
        table_start_row = row_index - len(tasks) - 2
        table_end_row = row_index - 1
        for col_index in range(1, len(headers) + 1):
            col_letter = get_column_letter(col_index)
            side = Side(border_style='thin', color='000000')
            border = Border(top=side, bottom=side, left=side, right=side)
            for row in range(table_start_row, table_end_row + 1):
                sheet.cell(row=row, column=col_index).border = border

        row_index += 1

    # Remove the default 'Sheet' that is automatically created when the workbook is initialized
    workbook.remove(workbook['Sheet'])

    # Create the response with the Excel file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f"attachment; filename=Task_Master_Data_{request.user.username}.xlsx"
    workbook.save(response)

    return response