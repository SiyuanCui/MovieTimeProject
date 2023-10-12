from django.urls import path
from reviewapp.views import RateMovie, ReviewDetail, likeHandle, deleteReview

urlpatterns = [
    path('<imdb_id>/rate', RateMovie, name='rate-movie'),
    path('<username>/<imdb_id>', ReviewDetail, name='review-detail'),
    path('review/<username>/delete/<imdb_id>/', deleteReview, name='delete-review'),
    path('<username>/<imdb_id>/<str:like_action>/', likeHandle, name='handle-like')
]