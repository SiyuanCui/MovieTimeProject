from django.contrib.auth import get_user_model
from django.test import TestCase
from authapp.forms import SignupForm


User = get_user_model()

class TestForms(TestCase):
    def test_signup_form_unique_username_validation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

