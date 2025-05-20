from django.apps import AppConfig

# Importing the AppConfig class from Django's apps module. This is the base class for configuring a Django application.


class TaskmasterConfig(AppConfig):
    # This class is used to configure the 'taskmaster' application.

    default_auto_field = 'django.db.models.BigAutoField'
    # Specifies the default type of primary key field to use for models in this app.
    # 'BigAutoField' is an integer field that automatically increments and is suitable for large datasets.

    name = 'taskmaster'
    # The name of the application. This should match the name of the app's directory.
