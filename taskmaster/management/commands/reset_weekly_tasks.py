from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from ...models import *


class Command(BaseCommand):
    # Description of the command
    help = 'Reset completed weekly tasks for all users on Monday at 00:00 based on user timezone'

    def handle(self, *args, **kwargs):
        """
        Handle method to reset completed weekly tasks for all users on Monday at 00:00 based on user timezone.

        Algorithm:
        1. Retrieve all user profiles.
        2. Loop through each user profile.
        3. Convert current datetime to user's timezone.
        4. Check if the current day is Monday and time is 00:00.
        5. If it's Monday at 00:00, reset completed weekly tasks for the user.
        """

        # Step 1: Retrieve all user profiles
        users = UserProfile.objects.all()  # Fetch all user profiles from the database

        for user in users:
            # Step 3: Get user's timezone from their profile
            # Convert user's timezone string to a timezone object
            tz = pytz.timezone(user.timezone)

            # Step 3: Convert current datetime to user's timezone
            now = timezone.now().astimezone(tz)  # Current datetime in user's timezone
            today = timezone.now().astimezone(tz).date()  # Current date in user's timezone

            # Step 4: Check if it is Monday at 00:00
            if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
                # Retrieve the weekly tasks for the user
                # Fetch all weekly tasks for the user
                weekly_tasks = Task.objects.filter(weekly=True, user=user.user)

                # Step 5: Create task history entries for completed weekly tasks
                TaskHistory.objects.bulk_create([
                    TaskHistory(
                        user=task.user,  # User associated with the task
                        title=task.title,  # Title of the task
                        description=task.description,  # Description of the task
                        execution_day=task.execution_day,  # Day the task was executed
                        execution_time=task.execution_time,  # Time the task was executed
                        completed=task.completed,  # Completion status of the task
                        task_type='weekly',  # Type of the task (weekly)
                        date=today  # Date of resetting the task
                    ) for task in weekly_tasks
                ])

                # Step 5: Reset completed weekly tasks to mark them as incomplete
                Task.objects.filter(user=user.user, completed=True, weekly=True).update(
                    completed=False)  # Update tasks

        # Print success message to the console
        self.stdout.write(self.style.SUCCESS(
            'Weekly tasks reset successfully.'))
