from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ..models import *

class UserLoginForm(AuthenticationForm):
    """Custom login form for users."""

    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegisterForm(UserCreationForm):
    """Custom user registration form with an additional 'fullname' field."""

    fullname = forms.CharField(max_length=255, label='fullname', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS class to the password field for styling
        self.fields["password1"].widget.attrs.update({"class": "form-style"})

    def clean_fullname(self):
        """Custom validation for the 'fullname' field to ensure it contains only alphabetic characters."""
        fullname = self.cleaned_data.get('fullname')
        if not fullname.isalpha():
            raise forms.ValidationError("Full name should only contain alphabetic characters.")
        return fullname

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'fullname']

class TaskForm(forms.ModelForm):
    """Custom form for creating or editing tasks with additional validation."""

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Set execution_time to required
        self.fields['execution_time'].required = True
        # Set execution_day to required if weekly is True
        self.fields['execution_day'].required = self.data.get('weekly')
        # Set execution_date to required if monthly is True
        self.fields['execution_date'].required = self.data.get('monthly')

    def clean(self):
        """Custom validation to ensure proper task configuration based on daily, weekly, or monthly execution."""
        cleaned_data = super().clean()
        daily = cleaned_data.get('daily')
        weekly = cleaned_data.get('weekly')
        monthly = cleaned_data.get('monthly')
        execution_day = cleaned_data.get('execution_day')
        execution_date = cleaned_data.get('execution_date')

        # Ensure at least one of daily, weekly, or monthly is True
        if not daily and not weekly and not monthly:
            raise ValidationError("At least one of 'Daily', 'Weekly', or 'Monthly' must be selected.")

        # Ensure only one of daily, weekly, or monthly is True
        options_count = sum([daily, weekly, monthly])
        if options_count != 1:
            raise ValidationError("Please select one and only one of 'Daily', 'Weekly', or 'Monthly'.")

        # Ensure execution_day is within the allowed list for weekly tasks
        allowed_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if weekly and execution_day not in allowed_days:
            raise ValidationError("Invalid 'Execution Day'. Please select a valid day of the week.")

        # Ensure execution_date is within the allowed range for monthly tasks
        if monthly and execution_date not in range(1, 32):
            raise ValidationError("Invalid 'Execution Date'. Please select a valid day (1 to 31).")

        # Ensure valid field for daily task
        if daily and (execution_day or execution_date):
            raise ValidationError("Invalid field for daily task.")

        # Ensure valid field for weekly task
        if weekly and execution_date:
            raise ValidationError("Invalid field for weekly task.")

        # Ensure valid field for monthly task
        if monthly and execution_day:
            raise ValidationError("Invalid field for monthly task.")

        return cleaned_data

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'daily', 'weekly', 'monthly', 'execution_day', 'execution_time', 'execution_date']
        widgets = {
            'execution_day': forms.Select(choices=[('', 'Select Day'), ('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                                                   ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                                   ('Friday', 'Friday'), ('Saturday', 'Saturday')]),
            'execution_time': forms.TimeInput(attrs={'type': 'time'}),
            'execution_date': forms.Select(choices=[('', 'Select Date')] + [(day, f'Day {day}') for day in range(1, 32)]),
        }
