from django.forms import ModelForm
from .models import Profile, Post

class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','city', 'image']

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
