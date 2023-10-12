from django.contrib import admin
from movieapp.models import Movie, Genre

# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)