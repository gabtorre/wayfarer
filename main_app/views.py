# external
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 

# internal
from .forms import Profile_Form
# Create your views here.

# main views
def home(request):
    return render(request, 'home.html')




# auth views

# show profile
def profile(request):
    return render(request, 'account/profile.html')


# sign up
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'regristration/signup.html', context)


# edit and update
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        try:
            profile_form = Profile_Form(request.POST, instance=user.profile)
            if profile_form.is_valid():
                profile_form.save()
        except:
            profile_form = Profile_Form(request.POST)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
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
