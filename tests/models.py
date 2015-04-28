from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class TestUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'username'
