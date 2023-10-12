from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import requests
from django.core.files import File
from io import BytesIO
import urllib.request
from django.core.files.base import ContentFile

class Actor(models.Model):
    actorname = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=False, unique=True)
    def __str__(self):
        return self.actorname

    def get_absolute_url(self):
        return reverse('actor-movie', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.actorname)
        return super().save(*args, **kwargs)


class Genre(models.Model):
    genrename = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=False, unique=True)
    def __str__(self):
        return self.genrename

    def get_absolute_url(self):
        return reverse('genre-movie', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genrename)
        return super().save(*args, **kwargs)



class Rating(models.Model):
    source = models.CharField(max_length=30)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.source


class Movie(models.Model):
    Title = models.CharField(max_length=150)
    Year = models.CharField(max_length=50, blank=True)
    Rated = models.CharField(max_length=10, blank=True)
    Released = models.CharField(max_length=50, blank=True)
    Runtime = models.CharField(max_length=20, blank=True)
    Genre = models.ManyToManyField(Genre, blank=True)
    Director = models.CharField(max_length=70, blank=True)
    Writer = models.CharField(max_length=200, blank=True)
    Actors = models.ManyToManyField(Actor, blank=True)
    Plot = models.TextField(max_length=900, blank=True)
    Language = models.CharField(max_length=100, blank=True)
    Poster = models.ImageField(upload_to='movies', blank=True)
    Poster_url = models.URLField(blank=True)
    Ratings = models.ManyToManyField(Rating, blank=True)
    imdbID = models.CharField(max_length=50, blank=True)
    Type = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        if not self.Poster and self.Poster_url:
            try:
                with urllib.request.urlopen(self.Poster_url) as response:
                    file_name = self.Poster_url.split("/")[-1]
                    image_data = response.read()
                    image_file = BytesIO(image_data)
                    self.Poster.save(file_name, File(image_file), save=False)
            except Exception as e:
                pass
        return super().save(*args, **kwargs)

