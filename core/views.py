from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from django.http import JsonResponse

def home_page(req):
    return render(req, 'core/base.html')


def tweet_list(request):
    query = request.GET.get('q')  # Get search query from request
    
    # Filter by username if query exists, else return all tweets
    if query:
        tweets = Tweet.objects.filter(user__username__icontains=query).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')

    paginator = Paginator(tweets, 20)  # Load 20 tweets initially
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle AJAX request for infinite scroll
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        tweets_data = [
            {
                'id': tweet.id,
                'user': tweet.user.username,
                'text': tweet.text,
                'img_url': tweet.img.url if tweet.img else None,
                'created_at': tweet.created_at.strftime('%b %d, %Y %H:%M'),
            }
            for tweet in page_obj
        ]
        return JsonResponse({
            'tweets': tweets_data,
            'has_next': page_obj.has_next()
        })

    return render(request, 'core/tweet_list.html', {
        'page_obj': page_obj,
        'show_search': True,
        'query': query,  # Pass query to template
    })


def my_tweets(request):
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(tweets, 10)  # Load 10 tweets initially
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle AJAX request for infinite scroll
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        tweets_data = [
            {
                'id': tweet.id,
                'user': tweet.user.username,
                'text': tweet.text,
                'img_url': tweet.img.url if tweet.img else None,
                'created_at': tweet.created_at.strftime('%b %d, %Y %H:%M'),
                'editable': tweet.user == request.user,  # Add editable info
            }
            for tweet in page_obj
        ]
        return JsonResponse({
            'tweets': tweets_data,
            'has_next': page_obj.has_next()
        })

    return render(request, 'core/my_tweets.html', {'page_obj': page_obj})


@login_required
def tweet_create(req):
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            # req.session.modified = True
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
            # req.session.modified = True
            messages.success(req, "Tweet updated successfully!")
            return redirect('my_tweets')
    else:
        form = TweetForm(instance=tweet)
    return render(req, 'core/tweet_form.html', {'form': form})


@login_required
def tweet_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    tweet.delete()
    # req.session.modified = True
    messages.success(req, "Tweet deleted successfully!")
    return redirect('my_tweets')


@login_required
def tweet_confirm_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    return render(req, 'core/tweet_confirm_delete.html', {'tweet': tweet})


def profile(req):
    return render(req, 'core/profile.html')


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
                return redirect('tweet_list')
        else:
            messages.error(req, 'Invalid User')
            return render(req, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(req, 'registration/login.html', {'form': form})


def logout_user(req):
    logout(req)
    return render(req, 'registration/logged_out.html')