from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path(
        'register/',
        views.UserRegistrationView.as_view(),
        name='user_register',
    ),
    path(
        'login/',
        views.UserLoginView.as_view(),
        name='user_login'
    ),
    path('logout/',
         views.UserLogoutView.as_view(),
         name='user_logout',
         ),
    path(
        'profile/<int:user_id>/',
        views.UserProfileView.as_view(),
        name='user_profile',
    ),
    path(
        'profile/edit/<int:user_id>/',
        views.UserProfileEdit.as_view(),
        name='user_profile_edit',
    ),
    path(
        'password/reset/',
        views.UserPasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'password/reset/done/',
        views.UserPasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'password/reset/confirm/<uidb64>/<token>/',
        views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'password/reset/complete/',
        views.UserPasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path(
        'follow/<int:user_id>/',
        views.UserFollowView.as_view(),
        name='user_follow',
    ),
    path(
        'unfollow/<int:user_id>/',
        views.UserUnFollowView.as_view(),
        name='user_unfollow',
    ),
]
