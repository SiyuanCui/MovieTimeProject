from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authapp.views import signin, signout, register, profile, profileEdit, changePassword, profileDetail

class TestUrls(SimpleTestCase):
    def test_signin_url_is_resolved(self):
        url=reverse('signin')
        self.assertEquals(resolve(url).func, signin)

    def test_signout_url_is_resolved(self):
        url=reverse('signout')
        self.assertEquals(resolve(url).func, signout)

    def test_register_url_is_resolved(self):
        url=reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_profile_url_is_resolved(self):
        url=reverse('profile', args=['some-string'])
        self.assertEquals(resolve(url).func, profile)

    def test_profileedit_url_is_resolved(self):
        url=reverse('profile-edit')
        self.assertEquals(resolve(url).func, profileEdit)

    def test_changepassword_url_is_resolved(self):
        url = reverse('change-password')
        self.assertEquals(resolve(url).func, changePassword)

    def test_profiledetail_url_is_resolved(self):
        username = 'testuser1'
        profile_type = 'Movie Reviewed'
        url = reverse('profile-detail', args=[username, profile_type])
        self.assertEquals(resolve(url).func, profileDetail)

