from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from ...models import *

class Command(BaseCommand):
    help = 'Reset completed daily tasks for all users at 00:00 based on user timezone'

    def handle(self, *args, **kwargs):
        users = UserProfile.objects.all()
        for user in users:
            tz = pytz.timezone(user.timezone) # Get user's timezone
            now = timezone.now().astimezone(tz)
            today = timezone.now().astimezone(tz).date()

            # Reset daily tasks at 00:00
            if now.hour == 11 :
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

        self.stdout.write(self.style.SUCCESS('Daily tasks reset successfully.'))