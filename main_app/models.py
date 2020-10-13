from django.db import models
from django.contrib.auth.models import User
from django_fields import DefaultStaticImageField
from django.core.files.storage import FileSystemStorage
fs=FileSystemStorage(location='media/images')
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.template.defaultfilters import slugify

# Make emails unique thanks to Quin

User._meta.get_field('email')._unique=True
User._meta.get_field('email')._blank=True

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=(models.CASCADE))
    image = models.ImageField(null=True, blank=True, upload_to = 'images', default = 'images/default.jpg')
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.user.username)
        return super().save(*args, **kwargs)

        def get_absolute_url(self):
            return reverse('profile', kwargs={'slug':self.slug})
    
    def __str__(self):
        return self.user.username


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    image = models.CharField(max_length=300)
    slug = models.SlugField(max_length=25, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('main', kwargs={'slug':self.slug})

    def __str__(self):
        return f"{self.name}, {self.country}"


class Post(models.Model):
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(max_length=2000, blank=False)
    image = models.ImageField(default = 'images/default.jpg', null=True, blank=True, upload_to = 'images')
    created_date = models.DateTimeField('date created', default=timezone.now)
    user = models.ForeignKey(User, on_delete=(models.CASCADE))
    city = models.ForeignKey(City, on_delete=(models.CASCADE))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['-created_date']


class Comment(models.Model):
    comment = models.TextField(max_length=200, blank=False)
    created_date = models.DateTimeField('date created', default=timezone.now)
    user = models.ForeignKey(User, on_delete=(models.CASCADE))
    post = models.ForeignKey(Post, on_delete=(models.CASCADE))

    def __str__(self):
        return f"{self.comment}"

    class Meta:
        ordering = ['-created_date']
    



    

