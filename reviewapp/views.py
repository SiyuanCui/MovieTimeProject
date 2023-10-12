from django.shortcuts import render, redirect, get_object_or_404
from movieapp.models import Movie
from reviewapp.forms import RateForm, CommentForm
from django.contrib.auth.models import User
from reviewapp.models import Review, CommentOnReview, Likes
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def RateMovie(request, imdb_id):
    movie = get_object_or_404(Movie, imdbID=imdb_id)
    user = request.user
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid() and isinstance(request.user, User):
            review_exists = Review.objects.filter(user=user, movie=movie).exists()
            if review_exists:
                messages.error(request, "you already rated this movie, you cannot review again!!!")
            else:
                rate = form.instance
                rate.stars = request.POST.get("stars")
                rate.user = request.user
                rate.movie = movie
                rate.save()
                return redirect('movie-details', imdb_id=imdb_id)
        else:
            return render(request, 'authapp/signin.html')

    else:
        form = RateForm()
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'reviewapp/rate_movie.html', context)


@login_required
def deleteReview(request, username, imdb_id):
    user = get_object_or_404(User, username=username)
    movie = get_object_or_404(Movie, imdbID=imdb_id)
    review = Review.objects.get(user=user, movie=movie)
    if request.user == review.user:
        review.delete()
    return redirect('movie-details', imdb_id=imdb_id)


def ReviewDetail(request, username, imdb_id):
    user = get_object_or_404(User, username=username)
    movie = get_object_or_404(Movie, imdbID=imdb_id)
    review = Review.objects.get(user=user, movie=movie)
    comments = review.comments.all().order_by('date')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.instance
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('review-detail', username=username, imdb_id=imdb_id)
    else:
        form = CommentForm()
    context = {
        'review': review,
        'movie': movie,
        'comments': comments,
        'form': form,
    }
    return render(request, 'reviewapp/review_detail.html', context)


def likeHandle(request, username, imdb_id, like_action):
    user_like_action = request.user
    if not isinstance(request.user, User):
        return render(request, 'authapp/signin.html')
    user_review = get_object_or_404(User, username=username)
    movie = get_object_or_404(Movie, imdbID=imdb_id)
    review = Review.objects.get(user=user_review, movie=movie)
    current_likes = review.likes
    current_unlikes = review.unlikes
    # 1 means like
    if like_action == 'like':
        liked = Likes.objects.filter(user=user_like_action, review=review, like_type=1).count()
        if liked == 1:
            Likes.objects.filter(user=user_like_action, review=review, like_type=1).delete()
            current_likes -= 1
        else:
            Likes.objects.create(user=user_like_action, review=review, like_type=1)
            current_likes += 1
    else:
        unliked = Likes.objects.filter(user=user_like_action, review=review, like_type=2).count()
        if unliked == 1:
            Likes.objects.filter(user=user_like_action, review=review, like_type=2).delete()
            current_unlikes -= 1
        else:
            Likes.objects.create(user=user_like_action, review=review, like_type=2)
            current_unlikes += 1
    review.likes = current_likes
    review.unlikes = current_unlikes
    review.save()
    return redirect('review-detail', username=username, imdb_id=imdb_id)




