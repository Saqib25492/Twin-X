from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    firstname = models.CharField(max_length=50, default='')
    lastname = models.CharField(max_length=50, default='')
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile.png')
    Location = models.CharField(max_length=100, blank=True)    
    
    def __str__(self) -> str:
        return self.user.username

class post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='post_images', default=' ')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now())
    no_of_likes = models.IntegerField(default=0) 
    
    def __str__(self) -> str:
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.user