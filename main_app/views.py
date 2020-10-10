# external
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required 
from django.views.generic import ListView
from django.core.paginator import Paginator

# internal
from .forms import Profile_Form, Post_Form
from .models import Post, City
# Create your views here.

""" TODO handle error messages """

# main views
def home(request):

    error_message = ''

    #   Login Post
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    #   Signup Post
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'

    return render(request, 'home.html')


# post create
def new_post(request, city_id):
    if request.method == 'POST':
        post_form = Post_Form(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.city = City.objects.get(id=city_id)
            new_post.save()
        return redirect('main', city_id)

# view/update post
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_form = Post_Form(request.POST, instance=post)
        if post_form.is_valid:
            post_form.save()
        return redirect('post', post_id)

    post_form = Post_Form(instance=post)
    context = {'post':post, 'post_form': post_form}
    return render(request, 'Post/post.html', context)

# delete post
def post_delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('profile')

def main(request, city_id):
    cities = City.objects.all()
    city = City.objects.get(id=city_id)
    posts = Post.objects.filter(city=city_id).order_by('-created_date')
    post_form = Post_Form()
    #posts = Post.objects.all()
    context = {'c_city':city, 'posts':posts, 'cities': cities, 'post_form':post_form}
    return render(request, 'main.html', context)


# auth views

# show profile
def profile(request):
    posts = Post.objects.filter(user=request.user.id)
    context = {'posts':posts}
    return render(request, 'account/profile.html', context)


# sign up
# def signup(request):
#     error_message = ''
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('profile')
#         else:
#             error_message = 'Invalid sign up - try again'
#     form = UserCreationForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'regristration/signup.html', context)


# edit and update
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        try:
            profile_form = Profile_Form(request.POST, request.FILES, instance=user.profile)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
                profile.image = request.FILES['image']
                new_profile.save()
        except:
            profile_form = Profile_Form(request.POST, request.FILES)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
                profile.image = request.FILES['image']
                new_profile.save()
        return redirect('profile')
    else:
        try:
            profile_form = Profile_Form(instance=user.profile)
            context = {'profile_form': profile_form}
            return render(request, 'account/edit.html', context)
        except:
            profile_form = Profile_Form()
            context = {'profile_form': profile_form}
            return render(request, 'account/edit.html', context)
