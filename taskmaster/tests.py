from django.test import TestCase
from django.urls import reverse
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