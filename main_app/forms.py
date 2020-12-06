from django import forms
from django.forms import ModelForm
from .models import Profile, Post, Comment

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','city', 'image', 'header_image']

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class Comment_Form(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

# found this online at  https://stackoverflow.com/questions/32860296/how-do-i-extend-usercreationform-to-include-email-field
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user