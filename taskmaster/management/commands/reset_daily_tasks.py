from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from ...models import *

class Command(BaseCommand):
    help = 'Reset completed daily tasks for all users at 00:00 based on user timezone'

    def handle(self, *args, **kwargs):
        """
        Handle the daily task reset command.

        This command is used to reset completed daily tasks for all users at 00:00 based on each user's timezone.
        """
        users = UserProfile.objects.all()
        for user in users:
            tz = pytz.timezone(user.timezone)  # Get user's timezone
            now = timezone.now().astimezone(tz)
            today = timezone.now().astimezone(tz).date()

            # Reset daily tasks at 00:00
            if now.hour == 0 and now.minute == 0:
                self._reset_daily_tasks(user, today)

        self.stdout.write(self.style.SUCCESS('Daily tasks reset successfully.'))

    def _reset_daily_tasks(self, user, today):
        """
        Reset completed daily tasks for a specific user.

        Args:
            user (UserProfile): The user for whom daily tasks are to be reset.
            today (datetime.date): The current date in the user's timezone.

        Returns:
            None
        """
        # Fetch and save daily tasks to history
        daily_tasks = Task.objects.filter(daily=True, user=user.user)
        TaskHistory.objects.bulk_create([
            TaskHistory(
                user=task.user,
                title=task.title,
                description=task.description,
                execution_time=task.execution_time,
                completed=task.completed,
                task_type='daily',
                date=today
            ) for task in daily_tasks
        ])

        # Reset completed daily tasks
        Task.objects.filter(user=user.user, completed=True, daily=True).update(completed=False)
