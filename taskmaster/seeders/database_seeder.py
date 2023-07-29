import random
from django.contrib.auth.models import User

def randomword(length=6):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choice(letters) for i in range(length))

def randomSentence():
    words = [randomword(random.randint(3, 8)) for _ in range(random.randint(5, 15))]
    return ' '.join(words)

def generate_random_user_data():
    names = ['John', 'Jane', 'Alice', 'Bob', 'Michael', 'Emily', 'David', 'Emma', 'Olivia', 'James']
    usernames = [f"{random.choice(names)}_{random.randint(100, 999)}" for _ in range(10)]

    return {
        'username': random.choice(usernames),
        'password': 'Password123',  # You can set a default password here
    }

def generate_random_task_data():
    titles = [randomword() for _ in range(10)]
    descriptions = [randomSentence() for _ in range(10)]
    execution_times = [f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}" for _ in range(10)]
    execution_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    task_type = ['daily', 'weekly', 'monthly']  
    random_task_type = random.choice(task_type)
    user = [user for user in User.objects.all()] 

    if random_task_type == 'daily':
        return {
            'title': random.choice(titles),
            'description': random.choice(descriptions),
            'execution_time': random.choice(execution_times),
            'daily': True,
            'completed': random.choice([True, False]),
            'user': random.choice(user)
        }
    elif random_task_type == 'weekly':
        return {
            'title': random.choice(titles),
            'description': random.choice(descriptions),
            'execution_day': random.choice(execution_days),  
            'execution_time': random.choice(execution_times),
            'weekly': True,
            'completed': random.choice([True, False]),
            'user': random.choice(user)
        }
    else:
        return {
            'title': random.choice(titles),
            'description': random.choice(descriptions),
            'execution_date': random.choice(range(1, 32)),  
            'execution_time': random.choice(execution_times),
            'monthly': True,  
            'completed': random.choice([True, False]),
            'user': random.choice(user)
        }
