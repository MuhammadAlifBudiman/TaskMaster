from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from ...models import *


class Command(BaseCommand):
    # Provide a brief description of the command's purpose
    help = 'Reset completed daily tasks for all users at 00:00 based on user timezone'

    def handle(self, *args, **kwargs):
        """
        Handle the daily task reset command.

        This command is used to reset completed daily tasks for all users at 00:00 based on each user's timezone.
        """
        # Fetch all user profiles
        users = UserProfile.objects.all()
        for user in users:
            # Get the user's timezone
            tz = pytz.timezone(user.timezone)
            # Get the current time in the user's timezone
            now = timezone.now().astimezone(tz)
            # Get the current date in the user's timezone
            today = timezone.now().astimezone(tz).date()

            # Check if the current time is exactly 00:00
            if now.hour == 0 and now.minute == 0:
                # Reset daily tasks for the user
                self._reset_daily_tasks(user, today)

        # Print a success message to the console
        self.stdout.write(self.style.SUCCESS(
            'Daily tasks reset successfully.'))

    def _reset_daily_tasks(self, user, today):
        """
        Reset completed daily tasks for a specific user.

        Args:
            user (UserProfile): The user for whom daily tasks are to be reset.
            today (datetime.date): The current date in the user's timezone.

        Returns:
            None
        """
        # Fetch all daily tasks for the user
        daily_tasks = Task.objects.filter(daily=True, user=user.user)

        # Save the daily tasks to the task history
        TaskHistory.objects.bulk_create([
            TaskHistory(
                user=task.user,  # Associate the task with the user
                title=task.title,  # Save the task title
                description=task.description,  # Save the task description
                execution_time=task.execution_time,  # Save the task execution time
                completed=task.completed,  # Save the task completion status
                task_type='daily',  # Mark the task type as daily
                date=today  # Save the current date
            ) for task in daily_tasks
        ])

        # Reset the completion status of daily tasks for the user
        Task.objects.filter(user=user.user, completed=True,
                            daily=True).update(completed=False)
