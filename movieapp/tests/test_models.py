from django.test import TestCase
from django.urls import reverse
from movieapp.models import Actor, Movie

class TestModels(TestCase):
    @classmethod
    def setUp(cls):
        Actor.objects.create(actorname='Test Actor')
        movie = Movie.objects.create(Title='Test Movie')

    def test_actorname_field(self):
        actor = Actor.objects.get(id=1)
        actorname = actor._meta.get_field('actorname')
        self.assertEqual(actorname.max_length, 100)
        self.assertTrue(actorname.unique)

    def test_slug_field(self):
        actor = Actor.objects.get(id=1)
        slug = actor._meta.get_field('slug')
        self.assertFalse(slug.null)
        self.assertTrue(slug.unique)

    def test_str_method(self):
        actor = Actor.objects.get(id=1)
        self.assertEqual(str(actor), 'Test Actor')

    def test_get_absolute_url_method(self):
        actor = Actor.objects.get(id=1)
        url = actor.get_absolute_url()
        expected_url = reverse('actor-movie', args=[actor.slug])
        self.assertEqual(url, expected_url)

    def test_save_method(self):
        actor = Actor.objects.get(id=1)
        actor.save()
        self.assertEqual(actor.slug, 'test-actor')

    def test_title_field(self):
        movie = Movie.objects.get(id=1)
        title = movie._meta.get_field('Title')
        self.assertEqual(title.max_length, 150)

    def test_str_method(self):
        movie = Movie.objects.get(id=1)
