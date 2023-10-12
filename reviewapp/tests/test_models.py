from django.test import TestCase
from django.contrib.auth.models import User
from movieapp.models import Movie
from reviewapp.models import Review, CommentOnReview, Likes

class TestModels(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.test_movie = Movie.objects.create(
            Title='Test Movie',
            Year='2021',
            imdbID='tt1234567',
        )
        self.test_review = Review.objects.create(
            user=self.test_user,
            movie=self.test_movie,
            stars=4,
        )

    def test_create_review(self):
        review = Review.objects.create(
            user=self.test_user,
            movie=self.test_movie,
            text='Test review text',
            stars=4,
        )
        self.assertEqual(review.user, self.test_user)
        self.assertEqual(review.movie, self.test_movie)
        self.assertEqual(review.text, 'Test review text')
        self.assertEqual(review.stars, 4)
        self.assertEqual(review.likes, 0)
        self.assertEqual(review.unlikes, 0)
        self.assertEqual(review.badge_level, 0)

    def test_get_default_comment(self):
        review = Review.objects.create(
            user=self.test_user,
            movie=self.test_movie,
            stars=3,
        )
        default_comment = review.get_default_comment()
        self.assertEqual(default_comment, "this user did not leave a review but just rate")

    def test_save_method(self):
        review = Review.objects.create(
            user=self.test_user,
            movie=self.test_movie,
            stars=15,
        )
        self.assertEqual(review.badge_level, 0)

        review.likes = 20
        review.save()
        self.assertEqual(review.badge_level, 2)


    def test_create_comment_on_review(self):
        comment = CommentOnReview.objects.create(
            review=self.test_review,
            user=self.test_user,
            body='Test comment body',
        )
        self.assertEqual(comment.review, self.test_review)
        self.assertEqual(comment.user, self.test_user)
        self.assertEqual(comment.body, 'Test comment body')


    def test_create_like(self):
        like = Likes.objects.create(
            review=self.test_review,
            user=self.test_user,
            like_type=1,
        )
        self.assertEqual(like.review, self.test_review)
        self.assertEqual(like.user, self.test_user)
        self.assertEqual(like.like_type, 1)


