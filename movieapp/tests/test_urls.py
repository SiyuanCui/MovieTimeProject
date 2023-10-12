from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from movieapp.views import index, movieDetails, watchedRemove, toWatchRemove, toWatchAdd, watchedAdd

User = get_user_model()


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url=reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_movie_url_is_resolved(self):
        url=reverse('movie-details', args=['tt2839419'])
        self.assertEquals(resolve(url).func, movieDetails)

    def test_add_watched_url_is_resolved(self):
        url=reverse('add-movies-to-watched', args=['tt2839419'])
        self.assertEquals(resolve(url).func, watchedAdd)

    def test_add_watch_url_is_resolved(self):
        url=reverse('add-movies-to-towatch', args=['tt2839419'])
        self.assertEquals(resolve(url).func, toWatchAdd)

    def test_remove_watched_url_is_resolved(self):
        url = reverse('remove-movies-watched', args=['tt2839419'])
        self.assertEquals(resolve(url).func, watchedRemove)

    def test_remove_watch_url_is_resolved(self):
        url = reverse('remove-movies-to-towatch', args=['tt2839419'])
        self.assertEquals(resolve(url).func, toWatchRemove)
