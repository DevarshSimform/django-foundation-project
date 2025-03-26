from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('list/', views.tweet_list, name='tweet_list'),
    path('mytweets/', views.my_tweets, name='my_tweets'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('mytweets/edit/<int:tweet_id>/', views.tweet_edit, name='tweet_edit'),
    path('mytweets/delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'),
    path('mytweets/delete/<int:tweet_id>/confirm/', views.tweet_confirm_delete, name='tweet_confirm_delete'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('users/', views.users_list, name='users_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('edit-profile', views.edit_profile, name='edit_profile')

    # path('search-users/', views.search_users, name='search_users'),
] 