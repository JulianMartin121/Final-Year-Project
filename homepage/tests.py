from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from unittest.mock import patch
from .models import CustomUser
from .views import (
    new_message, module1, module2, module3,
    course_material_1, course_material_2, course_material_3, home
)

class HomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_home_page_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'homepage/home.html')


class ModuleViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('accounts.signals.requests.post')
    def test_module1_view(self, mock_post):
        self.user = CustomUser.objects.create_user(username='testuser', password='Julian123', user_type='student')
        self.client.login(username='testuser', password='Julian123')
        module1_url = reverse('module1')
        response = self.client.get(module1_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/module1.html')

    @patch('accounts.signals.requests.post')
    def test_module2_view(self, mock_post):
        self.user = CustomUser.objects.create_user(username='testuser', password='Julian123', user_type='student')
        self.client.login(username='testuser', password='Julian123')
        module2_url = reverse('module2')
        response = self.client.get(module2_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/module2.html')

    @patch('accounts.signals.requests.post')
    def test_module3_view(self, mock_post):
        self.user = CustomUser.objects.create_user(username='testuser', password='Julian123', user_type='student')
        self.client.login(username='testuser', password='Julian123')
        module3_url = reverse('module3')
        response = self.client.get(module3_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/module3.html')


class CourseMaterialViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('accounts.signals.requests.post')
    def test_course_material_1_view(self, mock_post):
        self.teacher = CustomUser.objects.create_user(username='teacher', password='Julian123', user_type='teacher')
        self.client.login(username='teacher', password='Julian123')
        course_material_1_url = reverse('course_material_1')
        response = self.client.get(course_material_1_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/course_material_1.html')
        self.assertIn('students', response.context)

    @patch('accounts.signals.requests.post')
    def test_course_material_2_view(self, mock_post):
        self.teacher = CustomUser.objects.create_user(username='teacher', password='Julian123', user_type='teacher')
        self.client.login(username='teacher', password='Julian123')
        course_material_2_url = reverse('course_material_2')
        response = self.client.get(course_material_2_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/course_material_2.html')
        self.assertIn('students', response.context)

    @patch('accounts.signals.requests.post')
    def test_course_material_3_view(self, mock_post):
        self.teacher = CustomUser.objects.create_user(username='teacher', password='Julian123', user_type='teacher')
        self.client.login(username='teacher', password='Julian123')
        course_material_3_url = reverse('course_material_3')
        response = self.client.get(course_material_3_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/course_material_3.html')
        self.assertIn('students', response.context)

class URLTests(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_new_message_url_is_resolved(self):
        url = reverse('new_message')
        self.assertEqual(resolve(url).func, new_message)

    def test_module1_url_is_resolved(self):
        url = reverse('module1')
        self.assertEqual(resolve(url).func, module1)

    def test_module2_url_is_resolved(self):
        url = reverse('module2')
        self.assertEqual(resolve(url).func, module2)

    def test_module3_url_is_resolved(self):
        url = reverse('module3')
        self.assertEqual(resolve(url).func, module3)

    def test_course_material_1_url_is_resolved(self):
        url = reverse('course_material_1')
        self.assertEqual(resolve(url).func, course_material_1)

    def test_course_material_2_url_is_resolved(self):
        url = reverse('course_material_2')
        self.assertEqual(resolve(url).func, course_material_2)

    def test_course_material_3_url_is_resolved(self):
        url = reverse('course_material_3')
        self.assertEqual(resolve(url).func, course_material_3)