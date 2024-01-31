from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class AccountsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

        test_data = {
            'username': 'testuser2',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'user_type': '1',
            'uni_id': '123',
        }

        response = self.client.post(reverse('register'), test_data)
        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        test_data = {
            'username': 'testuser1',
            'password': '12345',
            'user_type': '1',
            'uni_id': '321',
        }

        response = self.client.post(reverse('login'), test_data)
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='32233')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_profile_view(self):
        self.client.login(username='testuser', password='442233')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')