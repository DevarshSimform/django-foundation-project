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
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),

    # path('search-users/', views.search_users, name='search_users'),
] 