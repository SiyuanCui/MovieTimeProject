from django.shortcuts import render, redirect, get_object_or_404
import requests
from movieapp.models import Movie, Actor, Genre, Rating
from django.utils.text import slugify
from authapp.models import Profile
from reviewapp.models import Review
from django.db.models import Avg
from django.core.paginator import Paginator
from django.contrib.auth.models import User


def index(request):
    query = request.GET.get('q')
    if query:
        url = 'https://www.omdbapi.com/?apikey=cc49745c&s=' + query
        response = requests.get(url)
        movie_data = response.json()
        print(movie_data)
        context = {
            'query': query,
            'movie_data': movie_data,
            'page_number': 1,
        }
        return render(request, 'movieapp/search_results.html', context)
    return render(request, 'movieapp/index.html')


def pagination(request, query, page_number):
    url = 'https://www.omdbapi.com/?apikey=cc49745c&s=' + query + '&page=' + str(page_number)
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1
    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number,
    }
    return render(request, 'movieapp/search_results.html', context)

def movieDetails(request, imdb_id):
    if Movie.objects.filter(imdbID=imdb_id).exists():
        inMydb = True
        movie_data = Movie.objects.get(imdbID=imdb_id)
        reviews = movie_data.reviews.all()
        reviews_avg = reviews.aggregate(Avg('stars'))
        reviews_count = reviews.count()

    else:
        inMydb = False
        url = 'https://www.omdbapi.com/?apikey=cc49745c&i=' + imdb_id
        response = requests.get(url)
        movie_data = response.json()

        actor_lists = []
        genre_lists = []
        rating_lists = []

        if 'Actors' in movie_data:
            actor_list = movie_data['Actors'].split(',')
            actor_list = [actor.strip() for actor in actor_list]
            for actor in actor_list:
                actor_slug = slugify(actor)
                a, created = Actor.objects.get_or_create(actorname=actor, slug=actor_slug)
                actor_lists.append(a)
        else:
            pass

        if 'Genre' in movie_data:
            genre_list = movie_data['Genre'].split(',')
            genre_list = [genre.strip() for genre in genre_list]

            for genre in genre_list:
                genre_slug = slugify(genre)
                g, created = Genre.objects.get_or_create(genrename=genre, slug=genre_slug)
                genre_lists.append(g)
        else:
            pass

        if 'Ratings' in movie_data:
            for rate in movie_data['Ratings']:
                r, created = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
                rating_lists.append(r)
        else:
            pass

        m, created = Movie.objects.get_or_create(
            Title=movie_data.get('Title', None),
            Year=movie_data.get('Year', None),
            Rated=movie_data.get('Rated', None),
            Released=movie_data.get('Released', None),
            Runtime=movie_data.get('Runtime', None),
            Director=movie_data.get('Director',None),
            Writer=movie_data.get('Writer',None),
            Plot=movie_data.get('Plot',None),
            Language=movie_data.get('Language',None),
            Poster_url=movie_data.get('Poster',None),
            imdbID=movie_data.get('imdbID', None),
            Type=movie_data.get('Type', None),
        )

        m.Genre.add(*genre_lists)
        m.Actors.add(*actor_lists)
        m.Ratings.add(*rating_lists)
        m.save()

        reviews = None
        reviews_avg = None
        reviews_count = None

    context = {
        'inMydb': inMydb,
        'movie_data': movie_data,
        'reviews': reviews,
        'reviews_avg': reviews_avg,
        'reviews_count': reviews_count,
    }
    return render(request, 'movieapp/movie_details.html', context)


def genre_movie(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    movie_data = Movie.objects.filter(Genre=genre)

    #Pagination
    paginator = Paginator(movie_data, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data':  movie_data,
        'genre': genre,
    }
    return render(request, 'movieapp/genre.html', context)


def actor_movie(request, actor_slug):
    actor = get_object_or_404(Actor, slug=actor_slug)
    movie_data = Movie.objects.filter(Actors=actor)

    # Pagination
    paginator = Paginator(movie_data, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'actor': actor,
    }
    return render(request, 'movieapp/actor.html', context)


def toWatchAdd(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    if not isinstance(request.user, User):
        return render(request, 'authapp/signin.html')
    profile = Profile.objects.get(user=request.user)
    profile.to_watch.add(movie)
    return redirect('movie-details', imdb_id=imdb_id)

def watchedAdd(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    if not isinstance(request.user, User):
        return render(request, 'authapp/signin.html')
    profile = Profile.objects.get(user=request.user)
    if profile.to_watch.filter(imdbID=imdb_id).exists():
        profile.to_watch.remove(movie)
    profile.watched.add(movie)
    return redirect('movie-details', imdb_id=imdb_id)

def toWatchRemove(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    profile = Profile.objects.get(user=request.user)
    profile.to_watch.remove(movie)
    return redirect('movie-details', imdb_id=imdb_id)

def watchedRemove(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    profile = Profile.objects.get(user=request.user)
    profile.watched.remove(movie)
    return redirect('movie-details', imdb_id=imdb_id)


