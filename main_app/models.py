from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    city = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=(models.CASCADE))

    def __str__(self):
        return self.user.username


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    image = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.name}, {self.country}"


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    image = models.CharField(max_length=300)

    user = models.ForeignKey(User, on_delete=(models.CASCADE))
    city = models.ForeignKey(City, on_delete=(models.CASCADE))

    def __str__(self):
        return f"{self.title}"


    



    

