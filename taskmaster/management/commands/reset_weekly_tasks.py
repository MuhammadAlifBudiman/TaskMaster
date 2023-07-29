from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from ...models import *

class Command(BaseCommand):
    help = 'Reset completed weekly tasks for all users on Monday at 00:00 based on user timezone'

    def handle(self, *args, **kwargs):
        users = UserProfile.objects.all()
        for user in users:
            tz = pytz.timezone(user.timezone) # Get user's timezone
            now = timezone.now().astimezone(tz)
            today = timezone.now().astimezone(tz).date()

            # Reset weekly tasks on Monday at 00:00
            if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
                weekly_tasks = Task.objects.filter(weekly=True, user=user.user)
                TaskHistory.objects.bulk_create([
                    TaskHistory(
                        user=task.user,
                        title=task.title,
                        description=task.description,
                        execution_day=task.execution_day,
                        execution_time=task.execution_time,
                        completed=task.completed,
                        task_type='weekly',
                        date=today
                    ) for task in weekly_tasks
                ])

                Task.objects.filter(user=user.user, completed=True, weekly=True).update(completed=False)

        self.stdout.write(self.style.SUCCESS('Weekly tasks reset successfully.'))


