from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from unittest.mock import patch
import json
from accounts import views
from django.db import IntegrityError
from accounts.forms import RegistrationForm, LoginForm

User = get_user_model()

class AccountsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
        self.home_url = reverse('home')

        self.user_data = {
            'username': 'testuser',
            'password1': 'Julian123',
            'password2': 'Julian123',
            'email': 'testuser@example.com'
        }
        with patch('accounts.signals.requests.post'):
            self.user = User.objects.create_user(username='testuser', password='Julian123')

    @patch('accounts.signals.requests.post')
    def test_register_view_get(self, mock_post):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    @patch('accounts.signals.requests.post')
    def test_login_view_get(self, mock_post):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    @patch('accounts.signals.requests.post')
    def test_login_view_post_valid(self, mock_post):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'Julian123'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, self.home_url)

    @patch('accounts.signals.requests.post')
    def test_login_view_post_invalid(self, mock_post):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    @patch('accounts.signals.requests.post')
    def test_logout_view(self, mock_post):
        self.client.login(username='testuser', password='Julian123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertRedirects(response, self.home_url)

    @patch('accounts.signals.requests.post')
    def test_profile_view_authenticated(self, mock_post):
        self.client.login(username='testuser', password='Julian123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    @patch('accounts.signals.requests.post')
    def test_profile_view_unauthenticated(self, mock_post):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login if not authenticated
        self.assertRedirects(response, f'{reverse("login")}?next={self.profile_url}')


User = get_user_model()

class SignalsTests(TestCase):
    
    @patch('accounts.signals.requests.post')
    def test_send_user_data_signal(self, mock_post):
        # Create a new user which should trigger the signal
        user = User.objects.create_user(
            username='testuser', 
            password='testpassword', 
            email='testuser@example.com',
            user_type='student',
            Uni_ID='123456'
        )

        # Check if the signal sent the correct data
        expected_data = {
            'user_type': 'student',
            'username': 'testuser',
            'Uni_ID': '123456',
            'email': 'testuser@example.com'
        }
        
        # Ensure that the mock_post was called once
        self.assertTrue(mock_post.called)
        self.assertEqual(mock_post.call_count, 1)

        # Get the actual data sent in the post request
        actual_data = json.loads(mock_post.call_args[1]['data'])

        # Check if the actual data matches the expected data
        self.assertEqual(actual_data, expected_data)
        self.assertEqual(mock_post.call_args[1]['headers'], {'Content-Type': 'application/json'})


class TestUrls(SimpleTestCase):

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, views.profile_view)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register_view)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login_view)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout_view)

CustomUser = get_user_model()

class CustomUserModelTests(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'Julian123',
            'email': 'testuser@example.com',
            'user_type': 'student',
            'Uni_ID': '1234567'
        }

    @patch('accounts.signals.requests.post')
    def test_create_custom_user(self, mock_post):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.user_type, 'student')
        self.assertEqual(user.Uni_ID, '1234567')
        mock_post.assert_called_once()

    @patch('accounts.signals.requests.post')
    def test_create_custom_user_with_duplicate_Uni_ID(self, mock_post):
        CustomUser.objects.create_user(**self.user_data)
        duplicate_user_data = self.user_data.copy()
        duplicate_user_data['username'] = 'testuser2'
        duplicate_user_data['email'] = 'testuser2@example.com'
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(**duplicate_user_data)
        mock_post.assert_called_once()

    @patch('accounts.signals.requests.post')
    def test_create_custom_user_with_duplicate_email(self, mock_post):
        CustomUser.objects.create_user(**self.user_data)
        duplicate_user_data = self.user_data.copy()
        duplicate_user_data['username'] = 'testuser2'
        duplicate_user_data['Uni_ID'] = '7654321'
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(**duplicate_user_data)
        mock_post.assert_called_once()

    @patch('accounts.signals.requests.post')
    def test_user_str(self, mock_post):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
        mock_post.assert_called_once()

    @patch('accounts.signals.requests.post')
    def test_user_permissions(self, mock_post):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.user_permissions.count(), 0)
        self.assertEqual(user.groups.count(), 0)
        mock_post.assert_called_once()

    @patch('accounts.signals.requests.post')
    def test_default_user_type(self, mock_post):
        user = CustomUser.objects.create_user(username='testuser2', password='Julian123', email='testuser2@example.com', Uni_ID='7654321')
        self.assertEqual(user.user_type, 'student')
        mock_post.assert_called_once()