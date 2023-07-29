from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...seeders.database_seeder import *
from ...models import *  

class Command(BaseCommand):
    help = 'Seed the database with random data'

    def handle(self, *args, **kwargs):
        num_tasks_records = 200  
        num_users_records = 0  

        for _ in range(num_users_records):
            user_data = generate_random_user_data()
            User.objects.create_user(**user_data)

        for _ in range(num_tasks_records):
            task_data = generate_random_task_data()
            Task.objects.create(**task_data)

        self.stdout.write(self.style.SUCCESS('Database seed success'))