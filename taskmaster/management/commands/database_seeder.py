from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...seeders.database_seeder import *  
from ...models import *  

class Command(BaseCommand):
    help = 'Seed the database with random data'

    def handle(self, *args, **kwargs):
        """
        Handle method for the custom management command.
        Seeds the database with random data for User and Task models.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            None
        """
        num_tasks_records = 2  # Number of Task records to be created
        num_users_records = 1  # Number of User records to be created

        # Creating random User records
        for _ in range(num_users_records):
            user_data = generate_random_user_data()  # Generate random user data using the database_seeder
            User.objects.create_user(**user_data)

        # Creating random Task records
        for _ in range(num_tasks_records):
            task_data = generate_random_task_data()  # Generate random task data using the database_seeder
            Task.objects.create(**task_data)

        self.stdout.write(self.style.SUCCESS('Database seed success'))
