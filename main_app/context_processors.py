from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
from .models import City

def add_my_login_form(request):
    return {
        'auth_form': AuthenticationForm(),
        'signup_form': UserCreationForm()
    }

def cities(request):
    cities = City.objects.all().order_by('name')
    return {'cities': cities}