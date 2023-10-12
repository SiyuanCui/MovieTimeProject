from django.urls import path
from authapp.views import signin, signout, register, profile, profileEdit, changePassword, profileDetail, deleteAccount
from movieapp.views import index
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('register/', register, name='register'),
    path('<username>/', profile, name='profile'),
    path('profile/edit/', profileEdit, name='profile-edit'),
    path('profile/change_password/', changePassword, name='change-password'),
    path('profile/<username>/<str:profile_type>/', profileDetail, name='profile-detail'),
    path('delete-account/', deleteAccount, name='delete-account'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authapp/password_reset.html"), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="authapp/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authapp/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authapp/password_reset_done.html"), name='password_reset_complete'),
]
