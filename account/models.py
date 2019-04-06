from django.db import models
from django.contrib.auth.models import AbstractUser
# from .managers import CustomUserManager


class User(AbstractUser):
    username = models.EmailField(unique=True)
    name = models.CharField(max_length=40, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']
    # objects = CustomUserManager()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.name
