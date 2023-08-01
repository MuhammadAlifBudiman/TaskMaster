from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from ...models import *

class Command(BaseCommand):
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

        users = UserProfile.objects.all()

        for user in users:
            # Get user's timezone
            tz = pytz.timezone(user.timezone)

            # Get current date and time in the user's timezone
            now = timezone.now().astimezone(tz)
            today = timezone.now().astimezone(tz).date()

            # Reset monthly tasks on the 1st day of the month at 00:00
            if now.day == 1 and now.hour == 0 and now.minute == 0:
                # Get monthly tasks for the user
                monthly_tasks = Task.objects.filter(monthly=True, user=user.user)

                # Create task history records for completed monthly tasks
                TaskHistory.objects.bulk_create([
                    TaskHistory(
                        user=task.user,
                        title=task.title,
                        description=task.description,
                        execution_date=task.execution_date,
                        execution_time=task.execution_time,
                        completed=task.completed,
                        task_type='monthly',
                        date=today
                    ) for task in monthly_tasks
                ])

                # Set completed status to False for monthly tasks
                Task.objects.filter(user=user.user, completed=True, monthly=True).update(completed=False)

        self.stdout.write(self.style.SUCCESS('Monthly tasks reset successfully.'))
