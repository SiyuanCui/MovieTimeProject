from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from movieapp.models import Movie
from django.dispatch import receiver

# Create your models here.
import os
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	picture = models.ImageField(upload_to='profile_images', blank=True, null=True, default='default_avatar.jpg')
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	profile_info = models.CharField(max_length=150, null=True, blank=True)
	date_created = models.DateField(auto_now_add=True)
	to_watch = models.ManyToManyField(Movie, related_name='towatch')
	watched = models.ManyToManyField(Movie, related_name='watched')

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=Profile)
def resize_profile_picture(sender, instance, **kwargs):
	if instance.picture:
		pic = Image.open(instance.picture.path)
		pic.thumbnail((250, 250), Image.LANCZOS)
		pic.save(instance.picture.path)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)



@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
	if created == False:
		instance.profile.save()
