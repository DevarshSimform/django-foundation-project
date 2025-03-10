from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

def home_page(req):
    return render(req, 'core/base.html') 


def tweet_list(req):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(req, 'core/tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(req):
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            messages.success(req, "Tweet created successfully!")
            return redirect('tweet_list')
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
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(req, 'core/tweet_form.html', {'form': form})


@login_required
def tweet_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    
    tweet.delete()
    messages.success(req, "Tweet deleted successfully!")
    return redirect('tweet_list')


def register(req):
    if req.method == 'POST':
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            login(req)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(req, 'registration/register.html', {'form': form})


def login(req):
    return render(req, 'registration/login.html')


def logout(req):
    return render(req, 'registration/logout.html')