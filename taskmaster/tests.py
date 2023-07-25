from django.test import TestCase, Client
from django.urls import reverse
import datetime
from parameterized import parameterized
from django.contrib.auth.models import User

from .models import *

# Create your tests here.
class RegistrationLoginTest(TestCase):
    def setUp(self):
        self.valid_username = 'testuser1'
        self.valid_password = 'Albert.23'
        user = User.objects.create_user(username=self.valid_username, password=self.valid_password)
        user.save()
        UserProfile.objects.create(user=user)


    @parameterized.expand([
        # Test missing field
        ('', '', '', '', ['This field is required.', 'This field is required.', 'This field is required.', 'This field is required.']),
        # Test invalid password: entirely numeric
        ('testuser', 'testuser2', '1234', '1234', ['This password is entirely numeric.', 'This password must contain at least 1 symbol: @, #, etc', 'This password is too common.', 'This password is too short. It must contain at least 8 characters.', 'This password must contain at least one lowercase letter: a-z.', 'This password must contain at least one uppercase letter: A-Z.']),
        # Test invalid password: missing digit
        ('testuser', 'testuser2', 'Albertt@', 'Albertt@', ['This password must contain at least one digit: 0-9.']),
        # Test password mismatch
        ('testuser', 'testuser2', 'Albert@23', 'password', ['The two password fields didn’t match.']),
        # Test full name contain digit
        ('testuser1', 'testuser2', 'Albert@23', 'Albert@23', ['Full name should only contain alphabetic characters.']),
        # Test existing username
        ('testuser', 'testuser1', 'Albert@23', 'Albert@23', ['A user with that username already exists.']),
    ])
    def test_invalid_registration(self, fullname, username, password1, password2, expected_errors):
        # Submit invalid registration form
        data = {
        	'fullname': fullname,
            'username': username,
            'password1': password1,
            'password2': password2,
        }
        response = self.client.post(reverse('register'), data)
        
        # Verify registration form errors
        self.assertEqual(response.status_code, 200)
        form = response.context['register_form']
        errors = [error for field_errors in form.errors.values() for error in field_errors]
        self.assertEqual(set(errors), set(expected_errors))
        # Verify the user is not created in the database
        if not username == 'testuser1':
        	self.assertFalse(User.objects.filter(username=username).exists())

    def test_valid_registration(self):
        # Submit valid registration form
        data = {
        	'fullname': 'testuser',
            'username': 'testuser2',
            'password1': self.valid_password,
            'password2': self.valid_password,
        }
        response = self.client.post(reverse('register'), data)
        
        # Verify successful registration and redirection to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        # Verify the user is created in the database
        self.assertTrue(User.objects.filter(username=self.valid_username).exists())

    def test_valid_login(self):
        # Submit valid login form
        data = {'username': self.valid_username, 'password': self.valid_password}
        response = self.client.post(reverse('login'), data)
        
        # Verify successful login and redirection to index page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        
        # Verify user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    @parameterized.expand([
        # Test missing field
        ('', '', ['This field is required.', 'This field is required.']),
        # Test invalid password
        ('testuser1', 'password',['Please enter a correct username and password. Note that both fields may be case-sensitive.']),
        # Test invalid username
        ('testuser2', 'Albert@23', ['Please enter a correct username and password. Note that both fields may be case-sensitive.']),
    ])
    def test_invalid_login(self, username, password, expected_errors):
        # Submit invalid login form with incorrect password
        data = {'username': username, 'password': password}
        response = self.client.post(reverse('login'), data)

        # Verify login form errors
        form = response.context['login_form']
        errors = [error for field_errors in form.errors.values() for error in field_errors]
        self.assertEqual(set(errors), set(expected_errors))

        # Verify user is not authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        # Log in the user
        self.client.login(username=self.valid_username, password=self.valid_password)
        
        # Submit logout form
        response = self.client.post(reverse('logout'))
        
        # Verify successful logout and redirection to index page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('auth'))
        
        # Verify user is not authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class AddTask(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        UserProfile.objects.create(user=self.user)
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    @parameterized.expand([
        # Test missing field including type
        ('','','', '', '', '', '', ''),
        # Test missing field for dailytask
        (True,'','', '', '', '', '', ''),
        # Test missing field for weeklytask
        ('',True,'', '', '', '', '', ''),
        # Test missing field for monthlytask
        ('','',True, '', '', '', '', ''),
        # Test invalid execution time for daily task
        (True,'','', 'title', 'description', 'invalid', 'Sunday', 1),
        # Test invalid execution time for weekly task
        ('',True,'', 'title', 'description', 'invalid', 'Sunday', 1),
        # Test invalid execution time for monthly task
        ('','',True, 'title', 'description', 'invalid', 'Sunday', 1),
        # Test invalid execution day
        ('',True,'', 'title', 'description', '20:20', 'invalid', 1),
        # Test invalid execution date
        ('','',True, 'title', 'description', '20:20', 'Sunday', 0),
        # Test wrong field in dailytask
        (True,'','', 'title', 'description', '20:20', 'Sunday', 1),
        # Test wrong field in weeklytask
        ('',True,'', 'title', 'description', '20:20', 'Sunday', 1),
        # Test wrong field in monthlytask
        ('',True,'', 'title', 'description', '20:20', 'Sunday', 1),
    ])
    def test_invalid_add_task(self, daily, weekly, monthly, title, description, execution_time, execution_day, execution_date):
        # Make a POST request to the add_task view with invalid data
        data = {
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly,
            'title': title,
            'description': description,
            'execution_time': execution_time,
            'execution_day': execution_day,
            'execution_date': execution_date
        }

        response = self.client.post(reverse('add_task'), data)
        
        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the task has not been created
        task = Task.objects.filter(title=title, user=self.user).exists()
        self.assertFalse(task)

        if daily:
            # Check if the response redirects to the 'dailytask' URL
            self.assertRedirects(response, reverse('dailytask'))
        elif weekly:
            # Check if the response redirects to the 'weeklytask' URL
            self.assertRedirects(response, reverse('weeklytask'))
        elif monthly:
            # Check if the response redirects to the 'monthlytask' URL
            self.assertRedirects(response, reverse('monthlytask'))
        else:
            # Check if the response redirects to the 'index' URL
            self.assertRedirects(response, reverse('index'))

    @parameterized.expand([
        # Test valid daily task
        (True,'','', 'daily', 'description', '20:20', '', ''),
        # Test valid weekly task
        ('',True,'', 'weekly', 'description', '20:20', 'Sunday', ''),
        # Test valid monthly task
        ('','',True, 'monthly', 'description', '20:20', '', 1),
    ])
    def test_valid_add_task(self, daily, weekly, monthly, title, description, execution_time, execution_day, execution_date):
        # Make a POST request to the add_task view with valid data
        data = {
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly,
            'title': title,
            'description': description,
            'execution_time': execution_time,
            'execution_day': execution_day,
            'execution_date': execution_date
        }

        response = self.client.post(reverse('add_task'), data)
        
        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the task has not been created
        task = Task.objects.filter(title=title, user=self.user).exists()
        self.assertTrue(task)

        if daily:
            # Check if the response redirects to the 'dailytask' URL
            self.assertRedirects(response, reverse('dailytask'))
        elif weekly:
            # Check if the response redirects to the 'weeklytask' URL
            self.assertRedirects(response, reverse('weeklytask'))
        elif monthly:
            # Check if the response redirects to the 'monthlytask' URL
            self.assertRedirects(response, reverse('monthlytask'))


class EditTask(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        UserProfile.objects.create(user=self.user)
        self.title = 'title'
        self.description = 'description'
        self.execution_time = '00:00'
        self.execution_day = 'Monday'
        self.execution_date = 31
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(user=self.user, title=self.title, description=self.description, execution_time=self.execution_time, execution_day=self.execution_day, execution_date=self.execution_date)

    @parameterized.expand([
        # Test missing field including type
        ('','','', '', '', '', '', ''),
        # Test missing field for dailytask
        (True,'','', '', '', '', '', ''),
        # Test missing field for weeklytask
        ('',True,'', '', '', '', '', ''),
        # Test missing field for monthlytask
        ('','',True, '', '', '', '', ''),
        # Test invalid execution time for daily task
        (True,'','', 'title', 'description', 'invalid', 'Sunday', 1),
        # Test invalid execution time for weekly task
        ('',True,'', 'title', 'description', 'invalid', 'Sunday', 1),
        # Test invalid execution time for monthly task
        ('','',True, 'title', 'description', 'invalid', 'Sunday', 1),
        # Test invalid execution day
        ('',True,'', 'title', 'description', '20:20', 'invalid', 1),
        # Test invalid execution date
        ('','',True, 'title', 'description', '20:20', 'Sunday', 0),
        # Test wrong field in dailytask
        (True,'','', 'title', 'description', '20:20', 'Sunday', 1),
        # Test wrong field in weeklytask
        ('',True,'', 'title', 'description', '20:20', 'Sunday', 1),
        # Test wrong field in monthlytask
        ('',True,'', 'title', 'description', '20:20', 'Sunday', 1),
    ])
    def test_invalid_edit_task(self, daily, weekly, monthly, title, description, execution_time, execution_day, execution_date):
        # Make a POST request to the edit_task view with invalid data
        data = {
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly,
            'title': title,
            'description': description,
            'execution_time': execution_time,
            'execution_day': execution_day,
            'execution_date': execution_date
        }

        response = self.client.post(reverse('edit_task', args=[self.task.id]), data)

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Refresh the task from the database
        self.task.refresh_from_db()

        # Convert string to date time object
        self.execution_time = datetime.time.fromisoformat(self.execution_time)

        # Check if the task's fields have not updated
        self.assertEqual(self.task.daily, False)
        self.assertEqual(self.task.weekly, False)
        self.assertEqual(self.task.monthly, False)
        self.assertEqual(self.task.title, self.title)
        self.assertEqual(self.task.description, self.description)
        self.assertEqual(self.task.execution_time, self.execution_time)
        self.assertEqual(self.task.execution_day, self.execution_day)
        self.assertEqual(self.task.execution_date, self.execution_date)

        if daily:
            # Check if the response redirects to the 'dailytask' URL
            self.assertRedirects(response, reverse('dailytask'))
        elif weekly:
            # Check if the response redirects to the 'weeklytask' URL
            self.assertRedirects(response, reverse('weeklytask'))
        elif monthly:
            # Check if the response redirects to the 'monthlytask' URL
            self.assertRedirects(response, reverse('monthlytask'))
        else:
            # Check if the response redirects to the 'index' URL
            self.assertRedirects(response, reverse('index'))


    @parameterized.expand([
        # Test valid daily task
        (True,'','', 'daily', 'description', '20:20', '', ''),
        # Test valid weekly task
        ('',True,'', 'weekly', 'description', '20:20', 'Sunday', ''),
        # Test valid monthly task
        ('','',True, 'monthly', 'description', '20:20', '', 1),
    ])
    def test_valid_edit_task(self, daily, weekly, monthly, title, description, execution_time, execution_day, execution_date):
        # Make a POST request to the edit_task view with valid data
        data = {
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly,
            'title': title,
            'description': description,
            'execution_time': execution_time,
            'execution_day': execution_day,
            'execution_date': execution_date
        }

        response = self.client.post(reverse('edit_task', args=[self.task.id]), data)

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Refresh the task from the database
        self.task.refresh_from_db()

        # Convert string to date time object
        execution_time = datetime.time.fromisoformat(execution_time)

        # Check if the task's fields have been updated
        self.assertEqual(self.task.daily, True if daily else False)
        self.assertEqual(self.task.weekly, True if weekly else False)
        self.assertEqual(self.task.monthly, True if monthly else False)
        self.assertEqual(self.task.title, title)
        self.assertEqual(self.task.description, description)
        self.assertEqual(self.task.execution_time, execution_time)
        self.assertEqual(self.task.execution_day, execution_day if weekly else None)
        self.assertEqual(self.task.execution_date, execution_date if monthly else None)

        if daily:
            # Check if the response redirects to the 'dailytask' URL
            self.assertRedirects(response, reverse('dailytask'))
        elif weekly:
            # Check if the response redirects to the 'weeklytask' URL
            self.assertRedirects(response, reverse('weeklytask'))
        elif monthly:
            # Check if the response redirects to the 'monthlytask' URL
            self.assertRedirects(response, reverse('monthlytask'))


class DeleteTask(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        UserProfile.objects.create(user=self.user)
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(user=self.user, daily=True, title='title', description='description', execution_time='00:00')


    def test_invalid_delete_task_not_found(self):
        # Attempt to delete a task that does not exist in the database
        invalid_task_id = 9999

        # Make a POST request to the delete_task view with an invalid task ID
        response = self.client.post(reverse('delete_task', args=[invalid_task_id]))

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)

        # Check if the task still exists in the database
        task = Task.objects.filter(id=self.task.id).exists()
        self.assertTrue(task)

    def test_invalid_delete_task_permission_denied(self):
        # Create a different user for testing (no permission to delete the task)
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        UserProfile.objects.create(user=other_user)

        # Simulate a login request for the different user
        self.client.login(username='otheruser', password='otherpassword')

        # Make a POST request to the delete_task view with the task's ID using the different user's authentication
        response = self.client.post(reverse('delete_task', args=[self.task.id]))

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)

        # Check if the task still exists in the database
        task = Task.objects.filter(id=self.task.id).exists()
        self.assertTrue(task)

    def test_valid_delete_task(self):
        # Make a POST request to the delete_task view with the task's ID
        response = self.client.post(reverse('delete_task', args=[self.task.id]))

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the task has been deleted from the database
        task = Task.objects.filter(id=self.task.id).exists()
        self.assertFalse(task)


class MarkCompleteTask(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        UserProfile.objects.create(user=self.user)
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(user=self.user, daily=True, title='title', description='description', execution_time='00:00')


    def test_invalid_mark_complete_task_not_found(self):
        # Attempt to delete a task that does not exist in the database
        invalid_task_id = 9999

        # Make a POST request to the mark_task_complete view with an invalid task ID
        response = self.client.post(reverse('mark_task_complete', args=[invalid_task_id]))

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)

        # Refresh the task from the database
        self.task.refresh_from_db()

        # Check if the task not completed
        task = Task.objects.get(id=self.task.id)
        self.assertFalse(task.completed)

    def test_invalid_delete_task_permission_denied(self):
        # Create a different user for testing (no permission to delete the task)
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        UserProfile.objects.create(user=other_user)

        # Simulate a login request for the different user
        self.client.login(username='otheruser', password='otherpassword')

        # Make a POST request to the mark_task_complete view with the task's ID using the different user's authentication
        response = self.client.post(reverse('mark_task_complete', args=[self.task.id]))

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)

        # Refresh the task from the database
        self.task.refresh_from_db()

        # Check if the task not completed
        task = Task.objects.get(id=self.task.id)
        self.assertFalse(task.completed)

    def test_valid_delete_task(self):
        # Make a POST request to the mark_task_complete view with the task's ID
        response = self.client.post(reverse('mark_task_complete', args=[self.task.id]))

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Refresh the task from the database
        self.task.refresh_from_db()

        # Check if the task not completed
        task = Task.objects.get(id=self.task.id)
        self.assertTrue(task.completed)