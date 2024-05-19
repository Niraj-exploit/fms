from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(null=True)
    is_futsal_owner = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, default="default-user-logo.png")
    user_team = models.ForeignKey('userHome.Team', on_delete=models.SET_NULL, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
