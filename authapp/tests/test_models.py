from django.contrib.auth import get_user_model
from django.test import TestCase
from authapp.models import Profile

User = get_user_model()

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_profile_signal(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_update_profile_signal(self):
        new_user = User.objects.create_user(username='newtestuser', password='newtestpassword')
        new_user.first_name = "New First Name"
        new_user.save()

        updated_profile = Profile.objects.get(user=new_user)
        self.assertEqual(updated_profile.user.first_name, new_user.first_name)
