from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
def add_my_login_form(request):
    return {
        'auth_form': AuthenticationForm(),
        'signup_form': UserCreationForm()
    }