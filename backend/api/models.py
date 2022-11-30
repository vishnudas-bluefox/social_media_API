from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class user(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=100)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class user_table(models.Model):
    user_id= models.IntegerField(default=0)
    bio = models.CharField(max_length=250,default="None")
    no_followers = models.IntegerField(default=0)
    no_following = models.IntegerField(default=0)
    no_post = models.IntegerField(default=0)

#removed table
class followers(models.Model):
    user_id = models.CharField(max_length=1000)
    follower_id= models.CharField(max_length=1000)
class following(models.Model):
    user_id = models.CharField(max_length=1000)
    follower_id= models.CharField(max_length=1000)

#creating post for by user
class post(models.Model):
    user_id=models.IntegerField(default=0)
    title = models.CharField(max_length=150)
    description= models.CharField(max_length=10000)
    no_like = models.IntegerField(default=0)
    no_comments = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

#creating like database
class like(models.Model):
    post_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
