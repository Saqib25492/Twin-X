from django.contrib import admin
from .models import Profile, post, LikePost, FollowersCount
# Register your models here.
admin.site.register(Profile)
admin.site.register(post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)