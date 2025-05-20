"""
This module provides utility functions to generate random data for testing purposes.
It includes functions to create random strings, sentences, user data, and task data.
"""

import random
from django.contrib.auth.models import User

# Function to generate a random string of lowercase letters of a given length


def randomword(length=6):
    """
    Generate a random string of lowercase letters.

    Args:
        length (int): The length of the string to generate. Default is 6.

    Returns:
        str: A random string of lowercase letters.
    """
    letters = "abcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choice(letters) for i in range(length))

# Function to generate a random sentence with a random number of random words


def randomSentence():
    """
    Generate a random sentence.

    Returns:
        str: A sentence composed of random words.
    """
    words = [randomword(random.randint(3, 8))
             for _ in range(random.randint(5, 15))]
    return ' '.join(words)

# Function to generate random user data for testing purposes


def generate_random_user_data():
    """
    Generate random user data.

    Returns:
        dict: A dictionary containing a random username and a default password.
    """
    names = ['John', 'Jane', 'Alice', 'Bob', 'Michael',
             'Emily', 'David', 'Emma', 'Olivia', 'James']
    usernames = [
        f"{random.choice(names)}_{random.randint(100, 999)}" for _ in range(10)]

    return {
        'username': random.choice(usernames),
        'password': 'Password123',  # Default password
    }

# Function to generate random task data for testing purposes


def generate_random_task_data():
    """
    Generate random task data.

    Randomly chooses whether the task is daily, weekly, or monthly.

    Returns:
        dict: A dictionary containing task details based on the type of task.
    """
    titles = [randomword() for _ in range(10)]
    descriptions = [randomSentence() for _ in range(10)]
    execution_times = [
        f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}" for _ in range(10)]
    execution_days = ['Monday', 'Tuesday', 'Wednesday',
                      'Thursday', 'Friday', 'Saturday', 'Sunday']
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
