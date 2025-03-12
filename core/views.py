from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate


def home_page(req):
    return render(req, 'core/base.html')


def tweet_list(req):
    query = req.GET.get('q', '').strip()
    tweets = Tweet.objects.all().order_by('-created_at')
    if query:
        tweets = tweets.filter(user__username__icontains = query)
    return render(req, 'core/tweet_list.html', {'tweets': tweets})


def my_tweets(req):
    tweets = Tweet.objects.filter(user = req.user).order_by('-created_at')
    return render(req, 'core/my_tweets.html', {'my_tweets': tweets})

@login_required
def tweet_create(req):
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            messages.success(req, "Tweet created successfully!")
            return redirect('my_tweets')
        pass
    else:
        form = TweetForm()
    return render(req, 'core/tweet_form.html', {'form': form})


@login_required
def tweet_edit(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = req.user)
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            messages.success(req, "Tweet updated successfully!")
            return redirect('my_tweets')

    else:
        form = TweetForm(instance=tweet)
    return render(req, 'core/tweet_form.html', {'form': form})


@login_required
def tweet_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    
    tweet.delete()
    messages.success(req, "Tweet deleted successfully!")
    return redirect('my_tweets')


def register(req):
    if req.method == 'POST':
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            login(req, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(req, 'registration/register.html', {'form': form})


def login_user(req):
    if req.method == 'POST':
        form = AuthenticationForm(req, data=req.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=uname, password=password)
            if user is not None:
                login(req, user)
                req.session.set_expiry(0)
                return redirect('tweet_list')
            else:
                messages.warning(req, 'Invalid user')
                return redirect('tweet_list')
        else:
            messages.warning(req, 'Invalid user')
            return redirect('tweet_list')
    else:
        form = AuthenticationForm()
        return render(req, 'registration/login.html', {'form': form})


def logout_user(req):
    logout(req)
    return render(req, 'registration/logged_out.html')