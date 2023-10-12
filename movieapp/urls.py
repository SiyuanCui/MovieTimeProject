from django.urls import path
from movieapp.views import index, movieDetails, genre_movie, actor_movie, toWatchAdd, watchedAdd, pagination, toWatchRemove, watchedRemove


urlpatterns = [
    path('index/', index, name='index'),
    path('', index, name='index'),
    path('search/<query>/page/<page_number>', pagination, name='pagination'),
    path('<imdb_id>',movieDetails, name='movie-details'),
    path('<imdb_id>/addtowacth', toWatchAdd, name='add-movies-to-towatch'),
	path('<imdb_id>/addwatched', watchedAdd, name='add-movies-to-watched'),
    path('<imdb_id>/removetowatch', toWatchRemove, name='remove-movies-to-towatch'),
    path('<imdb_id>/removewatched', watchedRemove, name='remove-movies-watched'),
    path('genres/<slug:genre_slug>', genre_movie, name='genre-movie'),
    path('actors/<slug:actor_slug>', actor_movie, name='actor-movie'),
]