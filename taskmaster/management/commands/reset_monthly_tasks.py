from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from ...models import *


class Command(BaseCommand):
    # Description of the command
    help = 'Reset completed monthly tasks for all users on the 1st day of the month at 00:00 based on user timezone'

    def handle(self, *args, **kwargs):
        """
        Handle the command execution.

        This function will reset completed monthly tasks for all users on the 1st day of the month at 00:00
        based on each user's timezone.

        Logic:
        - Fetch all user profiles.
        - Loop through each user profile.
        - Get the user's timezone and current date and time in the user's timezone.
        - If the current date is the 1st day of the month at 00:00, reset completed monthly tasks for the user.
        - Create task history records for completed monthly tasks.
        - Set completed status to False for monthly tasks.
        """

        # Fetch all user profiles
        users = UserProfile.objects.all()

        for user in users:
            # Get user's timezone from their profile
            tz = pytz.timezone(user.timezone)

            # Get current date and time in the user's timezone
            now = timezone.now().astimezone(tz)  # Current datetime in user's timezone
            today = timezone.now().astimezone(tz).date()  # Current date in user's timezone

            # Check if it is the 1st day of the month at 00:00
            if now.day == 1 and now.hour == 0 and now.minute == 0:
                # Fetch all monthly tasks for the user
                monthly_tasks = Task.objects.filter(
                    monthly=True, user=user.user)

                # Create task history records for completed monthly tasks
                TaskHistory.objects.bulk_create([
                    TaskHistory(
                        user=task.user,  # User associated with the task
                        title=task.title,  # Title of the task
                        description=task.description,  # Description of the task
                        execution_date=task.execution_date,  # Date the task was executed
                        execution_time=task.execution_time,  # Time the task was executed
                        completed=task.completed,  # Completion status of the task
                        task_type='monthly',  # Type of the task (monthly)
                        date=today  # Date of resetting the task
                    ) for task in monthly_tasks
                ])

                # Reset the completed status of monthly tasks to False
                Task.objects.filter(
                    user=user.user, completed=True, monthly=True).update(completed=False)

        # Print success message to the console
        self.stdout.write(self.style.SUCCESS(
            'Monthly tasks reset successfully.'))
