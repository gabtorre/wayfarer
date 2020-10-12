# external
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 

# internal
from .forms import Profile_Form, Post_Form
from .models import Post, City

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
            return redirect('profile_edit')
        else:
            context = {'signup_errors':signup_form.errors}
            return render(request, 'home.html', context)

    return render(request, 'home.html', {"is_true": False})

def login_redirect(request):
    home(request)
    return render(request, 'home.html', {"is_true": True})

# post create
@login_required(login_url='/login_redirect',)
def new_post(request, city_id):
    if request.method == 'POST':
        post_form = Post_Form(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.city = City.objects.get(id=city_id)
            new_post.image = request.FILES['image']
            new_post.save()
        return redirect('main', city_id)



# view/update post
@login_required(login_url='/login_redirect',)
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_form = Post_Form(request.POST, request.FILES, instance=post)
        if post_form.is_valid:
            post_form.save()
        return redirect('post', post_id)

    post_form = Post_Form(instance=post)
    context = {'post':post, 'post_form': post_form}
    return render(request, 'Post/post.html', context)

# delete post
@login_required(login_url='/login_redirect',)
def post_delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('profile')

@login_required(login_url='/login_redirect',)
def main(request, city_id):
    cities = City.objects.all()
    city = City.objects.get(id=city_id)
    # posts = Post.objects.filter(city=city_id)
    post_list = Post.objects.filter(city=city_id)
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
 
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    post_form = Post_Form()
    #posts = Post.objects.all()
    context = {'c_city':city, 'posts':posts, 'cities': cities, 'post_form':post_form, 'page':page}
    return render(request, 'main.html', context)


# auth views

# show profile
# @login_required
@login_required(login_url='/login_redirect',)
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
@login_required(login_url='/login_redirect',)
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        try:
            profile_form = Profile_Form(request.POST, request.FILES, instance=user.profile)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
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


# create url for login redirect
# redirect to home view that loads popup on page load