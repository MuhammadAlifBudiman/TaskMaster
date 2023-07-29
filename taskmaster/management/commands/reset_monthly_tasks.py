from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from ...models import *

class Command(BaseCommand):
    help = 'Reset completed monthly tasks for all users on the 1st day of the month at 00:00 based on user timezone'

    def handle(self, *args, **kwargs):
        users = UserProfile.objects.all()
        for user in users:
            tz = pytz.timezone(user.timezone) # Get user's timezone
            now = timezone.now().astimezone(tz)
            today = timezone.now().astimezone(tz).date()

            # Reset monthly tasks on the 1st day of the month at 00:00
            if now.day == 1 and now.hour == 0 and now.minute == 0:
                monthly_tasks = Task.objects.filter(monthly=True, user=user.user)
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

                Task.objects.filter(user=user.user, completed=True, monthly=True).update(completed=False)

        self.stdout.write(self.style.SUCCESS('Monthly tasks reset successfully.'))