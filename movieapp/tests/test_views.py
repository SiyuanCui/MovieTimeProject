from django.test import TestCase
from django.urls import reverse
from movieapp.models import Movie, Genre
from django.contrib.auth.models import User

class TestViews(TestCase):
    def setUp(self):
        self.test_genre = Genre.objects.create(genrename='Action', slug='action')
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.test_movie = Movie.objects.create(
            Title='Test Movie',
            Year='2021',
            Rated='PG-13',
            Released='2021-01-01',
            Runtime='120 min',
            Director='John Doe',
            Writer='Jane Smith',
            Plot='A test movie plot.',
            Language='English',
            Poster_url='https://example.com/poster.jpg',
            imdbID='tt1234567',
            Type='movie',
        )
        self.test_movie.Genre.add(self.test_genre)

    def test_movie_details_existing_movie(self):
        response = self.client.get(reverse('movie-details', args=[self.test_movie.imdbID]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_movie.Title)


    def test_genre_movie(self):
        # 对于已存在的Genre对象的情况
        response = self.client.get(reverse('genre-movie', args=[self.test_genre.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_genre.genrename)






