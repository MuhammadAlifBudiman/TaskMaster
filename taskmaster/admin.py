# Importing the admin module from Django to register models for the admin interface.
from django.contrib import admin

# Importing all models from the current package to register them with the admin site.
from .models import *

# Registering the Task model to make it manageable through the Django admin interface.
admin.site.register(Task)

# Registering the UserProfile model to make it manageable through the Django admin interface.
admin.site.register(UserProfile)

# Registering the TaskHistory model to make it manageable through the Django admin interface.
admin.site.register(TaskHistory)
