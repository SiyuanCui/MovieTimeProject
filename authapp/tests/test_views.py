from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.signin_url = reverse('signin')
        self.client.login(username='testuser', password='testpassword')


    def test_signin_valid_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_signin_invalid_user(self):
        response = self.client.post(reverse('signin'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authapp/signin.html')
        self.assertContains(response, 'username and password is not matched')

    def test_signout(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_register_invalid_form(self):
        response = self.client.post(reverse('register'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authapp/register.html')
        self.assertContains(response, 'This field is required.')

    def test_register_get_request(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authapp/register.html')


