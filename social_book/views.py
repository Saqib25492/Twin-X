from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, post, LikePost, FollowersCount
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
import random


# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)     
    user_following = FollowersCount.objects.filter(follower = request.user.username)
    user_following_list = [users.user for users in user_following]
    
    feed = [post.objects.filter(user=usernames) for usernames in user_following_list]
    feed_list = list(chain(*feed))
    
    #User Suggestion
    all_users = User.objects.all()
    user_following_all = []
    
    for user in user_following:
        user_list = User.objects.get(username = user.user)
        user_following_all.append(user_list)
    
    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))] 
    current_user = User.objects.filter(username = request.user.username)
    final_suggestion_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestion_list)
    
    username_profile = [user.id for user in final_suggestion_list]
    username_profile_list = [Profile.objects.filter(id_user = ids) for ids in username_profile]
    
    suggestions_username_profile_list = list(chain(*username_profile_list)) 
    print(suggestions_username_profile_list)   
    return render(request, 'index.html', {'user_profile' : user_profile, 'posts': feed_list, 'Suggestions':suggestions_username_profile_list})

@login_required(login_url='signin')
def settings(request):
    # With this we are getting the user that is currently logged in
    user_profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            print(location)
            user_profile.profileimg = image
            user_profile.firstname = firstname
            user_profile.lastname = lastname
            user_profile.bio = bio
            user_profile.Location = location
            user_profile.save()
            
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            print('image loaded:', image)
            print(firstname)
            
            user_profile.profileimg = image
            user_profile.firstname = firstname
            user_profile.lastname = lastname
            user_profile.bio = bio
            user_profile.Location = location
            user_profile.save()
        
        return redirect('settings') 

    return render(request, 'setting.html', {'user_profile': user_profile})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username= username, password = password)
        if user is not None:
            auth.login(request, user)   
            return redirect('/')
        
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
        
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'User Exists')
                return redirect('signup')
            
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Invalid Username')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password = password1)
                auth.login(request, user_login)
                
                #create a Profile for the new user
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                messages.info(request, 'Succesfully registered')
                return redirect('settings') 
            
        else:
            messages.info(request, 'Password does not match')
            return redirect('signup')
    
    return render(request, 'signup.html')
 
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('Caption')
        
        new_post = post.objects.create(user = user, image = image, caption = caption)
        new_post.save()
        return redirect('/')
        
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    Post = post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id = post_id, username=username).first()   
    
    if like_filter == None:
        print('Inside like')
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        Post.no_of_likes += 1
        Post.save()
        return redirect('/')
    
    else:
        like_filter.delete()
        Post.no_of_likes -= 1
        Post.save()
        return redirect('/')
    
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)   
    user_post = post.objects.filter(user = pk)
    user_post_length = len(user_post)
    follower = request.user.username
    user = pk
    if FollowersCount.objects.filter(follower=follower, user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
        
    no_of_followers = len(FollowersCount.objects.filter(user = pk))
    user_following = len(FollowersCount.objects.filter(follower = pk))
    followers = FollowersCount.objects.filter(user = pk)
    followers = [follower.follower for follower in followers]

    
    
    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_post': user_post,
        'user_post_length':user_post_length,
        'no_of_followers': no_of_followers,
        'button_text':button_text,
        'user_following': user_following,
        'followers': followers,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')
        
        if FollowersCount.objects.filter(follower=follower, user = user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user = user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user = user)
            new_follower.save()

            return redirect('/profile/'+user)
        
    else: 
        return redirect('/')
    
@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        username = request.POST.get('username')
        username_object = User.objects.filter(username__icontains=username)
        username_profile = [users.id for users in username_object]
        username_profile_list = [Profile.objects.filter(id_user = id) for id in username_profile]
        
        username_profile_list = list(chain(*username_profile_list))
        
    return render(request, 'search.html',{'user_profile': user_profile, 'username_profile_list': username_profile_list})