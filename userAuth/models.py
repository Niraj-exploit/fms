from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10,null=True, blank=True)
    bio = models.TextField(null=True)
    is_futsal_owner = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
