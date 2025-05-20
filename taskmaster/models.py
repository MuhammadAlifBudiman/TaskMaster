"""
Models for the TaskMaster application.

This module defines the database models used in the TaskMaster application, including tasks, user profiles, and task history.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Task(models.Model):
    """
    Represents a task created by a user.

    Attributes:
        user (ForeignKey): The user who owns the task.
        title (CharField): The title of the task.
        description (TextField): A detailed description of the task.
        completed (BooleanField): Indicates whether the task is completed.
        created_at (DateTimeField): The timestamp when the task was created.
        daily (BooleanField): Indicates if the task is a daily task.
        weekly (BooleanField): Indicates if the task is a weekly task.
        monthly (BooleanField): Indicates if the task is a monthly task.
        execution_day (CharField): The day of the week for task execution (if applicable).
        execution_time (TimeField): The time of day for task execution (if applicable).
        execution_date (PositiveIntegerField): The date of the month for task execution (if applicable).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    daily = models.BooleanField(default=False)
    weekly = models.BooleanField(default=False)
    monthly = models.BooleanField(default=False)
    execution_day = models.CharField(max_length=9, blank=True, null=True)
    execution_time = models.TimeField(null=True, blank=True)
    execution_date = models.PositiveIntegerField(null=True, blank=True, validators=[
                                                 MinValueValidator(1), MaxValueValidator(31)])

    def __str__(self):
        """Returns the string representation of the task, which is its title."""
        return self.title


class UserProfile(models.Model):
    """
    Represents additional information about a user.

    Attributes:
        user (OneToOneField): The user associated with this profile.
        timezone (CharField): The timezone of the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, default='UTC')


class TaskHistory(models.Model):
    """
    Represents the history of tasks completed by a user.

    Attributes:
        DATE_TYPE_CHOICES (tuple): Choices for the type of task (daily, weekly, monthly).
        user (ForeignKey): The user who completed the task.
        title (CharField): The title of the task.
        description (TextField): A detailed description of the task.
        execution_day (CharField): The day of the week the task was executed (if applicable).
        execution_time (TimeField): The time of day the task was executed (if applicable).
        execution_date (PositiveIntegerField): The date of the month the task was executed (if applicable).
        completed (BooleanField): Indicates whether the task was completed.
        task_type (CharField): The type of task (daily, weekly, or monthly).
        date (DateField): The date the task was completed.
    """
    DATE_TYPE_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    execution_day = models.CharField(max_length=9, blank=True, null=True)
    execution_time = models.TimeField(null=True, blank=True)
    execution_date = models.PositiveIntegerField(null=True, blank=True, validators=[
                                                 MinValueValidator(1), MaxValueValidator(31)])
    completed = models.BooleanField(default=False)
    task_type = models.CharField(max_length=10, choices=DATE_TYPE_CHOICES)
    date = models.DateField()

    def __str__(self):
        """Returns the string representation of the task history, which includes the date and title."""
        return f"{self.date} - {self.title}"
