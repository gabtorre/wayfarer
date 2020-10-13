# external
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# internal
from .forms import Profile_Form, Post_Form
from .models import Post, City, Profile

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# main views
def home(request):
    #   Signup Post
    if request.method == 'POST' and request.POST['form_name'] == 'signup_form':  
        print(f"request {request.POST}")
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('profile_edit')
        else:
            context = {'signup_errors':signup_form.errors}
            return render(request, 'home.html', context)

    #   Login Post
    if request.method == 'POST' and request.POST['form_name'] == 'login_form':
        print(f"request {request.POST}")
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile', user.profile.slug)
        else:
            context = {'login_errors': form.errors}
            return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')



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
            if request.FILES:
                new_post.image = request.FILES['image']
            new_post.save()
        city = City.objects.get(id=city_id)
        return redirect('main', city.slug)



# view/update post
@login_required(login_url='/login_redirect',)
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_form = Post_Form(request.POST, instance=post)
        if post_form.is_valid():
            u_post = post_form.save(commit=False)
            if request.FILES:
                u_post.image = request.FILES['image']
            else:
                u_post.image = ('images/default.jpg')
            u_post.save()
        return redirect('post', post_id)

    post_form = Post_Form(instance=post)
    context = {'post':post, 'post_form': post_form}
    return render(request, 'Post/post.html', context)

# delete post
@login_required(login_url='/login_redirect',)
def post_delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('profile', request.user.profile.slug)

#render main page
@login_required(login_url='/login_redirect',)
def main(request, slug):
    cities = City.objects.all()
    city = City.objects.get(slug=slug)
    post_list = Post.objects.filter(city=city.id)
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
 
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    post_form = Post_Form()
    context = {'c_city':city, 'posts':posts, 'cities': cities, 'post_form':post_form, 'page':page}
    return render(request, 'main.html', context)

def city(request):
    cities = City.objects.all()
    return redirect('main', cities[0].slug)


# auth views

# show profile
@login_required(login_url='/login_redirect',)
def profile(request, slug):
    t_profile = Profile.objects.get(slug=slug)
    t_user = User.objects.get(id=t_profile.user_id)
    posts = Post.objects.filter(user=t_user.id)
    if t_user == request.user:
        auth=True
    else:
        auth=False
    context = {'posts':posts, 't_user':t_user, 'auth':auth}
    return render(request, 'account/profile.html', context)


# edit and update
@login_required(login_url='/login_redirect',)
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        try:
            profile_form = Profile_Form(request.POST, instance=user.profile)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
                if request.FILES:
                    new_profile.image = request.FILES['image']
                else:
                    new_profile.image = 'images/default.jpg'
                new_profile.save()
        except:
            profile_form = Profile_Form(request.POST)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
                if request.FILES:
                    new_profile.image = request.FILES['image']
                new_profile.save()
        return redirect('profile', request.user.profile.slug)
    else:
        try:
            profile_form = Profile_Form(instance=user.profile)
            context = {'profile_form': profile_form}
            return render(request, 'account/edit.html', context)
        except:
            profile_form = Profile_Form()
            context = {'profile_form': profile_form}
            return render(request, 'account/edit.html', context)

