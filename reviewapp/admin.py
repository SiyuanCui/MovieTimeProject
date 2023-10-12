from django.contrib import admin
from reviewapp.models import Review, CommentOnReview
# Register your models here.

admin.site.register(Review)
admin.site.register(CommentOnReview)