from django.db import models
from django.contrib.auth.models import User
from movieapp.models import Movie
# Create your models here.


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000, blank=True, default="this user did not leave a review but just rate")
    stars = models.SmallIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    unlikes = models.PositiveIntegerField(default=0)
    badge_level = models.SmallIntegerField(default=0)
    def __str__(self):
        return self.user.username
    def get_default_comment(self):
        return "this user did not leave a review but just rate"
    def save(self, *args, **kwargs):
        self.badge_level = self.likes // 10
        super().save(*args, **kwargs)





class CommentOnReview(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	body = models.TextField(max_length=1000)


class Likes(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='liked_review')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_user')
	like_type = models.PositiveSmallIntegerField()
