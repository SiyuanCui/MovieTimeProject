from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from authapp.models import Profile


class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name','last_name', 'password1', 'password2')

	def __int__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].error_messages = {'unique':'username already exists'}


class EditProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	location = forms.CharField(widget=forms.TextInput(), max_length=25, required=False)
	profile_info = forms.CharField(widget=forms.TextInput(), max_length=150, required=False)
	class Meta:
		model = Profile
		fields = ('picture', 'first_name', 'last_name', 'location',  'profile_info')


