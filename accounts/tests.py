from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class TestLogin(TestCase):

    def setUp(self):
        User.objects.create_user(
            email="john@example.com",
            password="haxOr863"
        )

    def test_loads_properly(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Login')
        self.assertEqual(response.status_code, 200)
        
    def test_success(self):
        data = {"username": "john@example.com", "password": "haxOr863"}
        response = self.client.post(reverse('login'), data, follow=True)
        self.assertRedirects(response, reverse('home'))
        
    def test_failure(self):
        data = {"username": "john@example.com", "password": "wront-pwd"}
        response = self.client.post(reverse('login'), data, follow=True)

        self.assertContains(response, 
            'Please enter a correct email address and password')
        self.assertEqual(response.status_code, 200)
        

class TestSignup(TestCase):

    def test_success(self):
        data = {
            "email": "john@example.com", 
            "password1": "haxOr863",
            "password2": "haxOr863"
        }
        response = self.client.post(reverse('signup'), data, follow=True)

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(email='john@example.com').exists())
        
    def test_loads_properly(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'Sign Up')
        self.assertEqual(response.status_code, 200)
        
    def test_failure_email(self):
        data = {
            "email": "john", 
            "password1": "haxOr863",
            "password2": "haxOr863"
        }
        response = self.client.post(reverse('signup'), data, follow=True)

        self.assertContains(response, 'Enter a valid email address')
        self.assertEqual(response.status_code, 200)


    def test_failure_password_mismatch(self):
        data = {
            "email": "john", 
            "password1": "haxOr863",
            "password2": "some-other"
        }
        response = self.client.post(reverse('signup'), data, follow=True)

        self.assertContains(response, 
            'The two password fields didn&#39;t match')
        self.assertEqual(response.status_code, 200)

