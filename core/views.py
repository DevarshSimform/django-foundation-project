from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm

def home_page(req):
    return render(req, 'core/base.html') 


def tweet_list(req):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(req, 'core/tweet_list.html', {'tweets': tweets})


def tweet_create(req):
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            return redirect('tweet_list')
        pass
    else:
        form = TweetForm()
    return render(req, 'core/tweet_form.html', {'form': form})


def tweet_edit(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = req.user)
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES, instance=tweet)
        if form.is_valid:
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(req, 'core/tweet_form.html', {'form': form})


def tweet_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    if req.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(req, 'core/tweet_confirm_delete.html', {'tweet': tweet})
