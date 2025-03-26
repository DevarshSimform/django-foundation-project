from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    img = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username 
    
# Commit msg of models creations 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.webp', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    # For storing followers and following
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
    )

    def __str__(self):
        return self.user.username
    
    def is_following(self, profile):
        return self.following.filter(id=profile.id).exists()

    def follow(self, profile):
        if not self.is_following(profile):
            self.following.add(profile)

    def unfollow(self, profile):
        if self.is_following(profile):
            self.following.remove(profile)
    
    def followers_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()