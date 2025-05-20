from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
# Import functions for generating random data
from ...seeders.database_seeder import *
from ...models import *  # Import models for database operations


class Command(BaseCommand):
    """
    Custom management command to seed the database with random data.
    This command creates random User and Task records for testing purposes.
    """

    help = 'Seed the database with random data'  # Description of the command

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
        num_tasks_records = 20  # Number of Task records to be created
        num_users_records = 5  # Number of User records to be created

        # Creating random User records
        for _ in range(num_users_records):
            # Generate random user data using the database_seeder
            user_data = generate_random_user_data()
            # Create a new User record in the database
            User.objects.create_user(**user_data)

        # Creating random Task records
        for _ in range(num_tasks_records):
            # Generate random task data using the database_seeder
            task_data = generate_random_task_data()
            # Create a new Task record in the database
            Task.objects.create(**task_data)

        # Print a success message to the console
        self.stdout.write(self.style.SUCCESS('Database seed success'))
