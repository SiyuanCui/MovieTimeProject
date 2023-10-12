from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from authapp.forms import SignupForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from authapp.models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from reviewapp.models import Review
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Max


def signin(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'authapp/signin.html', {'error':'username and password is not matched'})
        else:
            auth.login(request,user)
            return redirect('index')

    else:
        return render(request, 'authapp/signin.html')


def signout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        registerForm = SignupForm(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            user = authenticate(username=registerForm.cleaned_data['username'], password = registerForm.cleaned_data['password1'])
            user.email = registerForm.cleaned_data['email']
            user.first_name = registerForm.cleaned_data['first_name']
            user.last_name = registerForm.cleaned_data['last_name']
            messages.success(request, 'account was created for' + user.username)
            return redirect('signin')
    else:
        registerForm = SignupForm()

    context = {
        'registerForm': registerForm
    }
    return render(request, 'authapp/register.html', context)


@login_required(login_url='signin')
def profileEdit(request):
    profile = Profile.objects.get(user=request.user)
    username = request.user.username
    print('get request')
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.picture = form.cleaned_data['picture']
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.location = form.cleaned_data['location']
            profile.profile_info = form.cleaned_data['profile_info']
            profile.save()

            return redirect(reverse('profile', args=[username]))
    else:
        form = EditProfileForm()
    context = {
        'form': form,
    }
    return render(request, 'authapp/profile_edit.html', context)


@login_required(login_url='signin')
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'form':form,
        'user': request.user
    }
    return render(request, 'authapp/change_password.html', context)

@login_required(login_url='signin')
def profile(request, username):
    profile = request.user.profile
    movie_watched_count = profile.watched.filter(Type='movie').count()
    series_watched_count = profile.watched.filter(Type='series').count()
    watch_list_count = profile.to_watch.all().count()
    movie_reviewed_count = Review.objects.filter(user=request.user).count()
    reviews = Review.objects.filter(user=request.user)
    highest_badge_level = reviews.aggregate(Max('badge_level'))['badge_level__max']
    context = {
        'profile': profile,
        'movie_watched_count': movie_watched_count,
        'series_watched_count': series_watched_count,
        'watch_list_count': watch_list_count,
        'movie_reviewed_count': movie_reviewed_count,
        'highest_badge_level': highest_badge_level,
    }
    return render(request, 'authapp/profile.html', context)

@login_required()
def profileDetail(request, username, profile_type):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    movie_watched_count = profile.watched.filter(Type='movie').count()
    series_watched_count = profile.watched.filter(Type='series').count()
    watch_list_count = profile.to_watch.all().count()
    movie_reviewed_count = Review.objects.filter(user=user).count()
    list_title = profile_type
    reviews = Review.objects.filter(user=request.user)
    highest_badge_level = reviews.aggregate(Max('badge_level'))['badge_level__max']
    if profile_type == 'Movies Watched':
        movies = profile.watched.filter(Type='movie')
    elif profile_type == 'Series Watched':
        movies = profile.watched.filter(Type='series')
    elif profile_type == 'Watch list':
        movies = profile.to_watch.all()
    else:
        movies = Review.objects.filter(user=user)

    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
		'profile': profile,
        'movie_watched_count': movie_watched_count,
        'series_watched_count': series_watched_count,
        'watch_list_count': watch_list_count,
        'movie_reviewed_count': movie_reviewed_count,
        'list_title': list_title,
        'movie_data': movie_data,
        'highest_badge_level': highest_badge_level,
    }

    return render(request, 'authapp/profile.html', context)


@login_required
def deleteAccount(request):
    user = request.user
    profile = user.profile
    user.delete()
    profile.delete()
    auth.signout(request)
    return redirect('index')











