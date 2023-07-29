from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Task(models.Model):
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
    execution_date = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(31)])

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, default='UTC')

class TaskHistory(models.Model):
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
    execution_date = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(31)])
    completed = models.BooleanField(default=False)
    task_type = models.CharField(max_length=10, choices=DATE_TYPE_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.title}"