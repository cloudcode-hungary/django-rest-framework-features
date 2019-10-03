from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class User(PermissionsMixin, AbstractBaseUser):
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        verbose_name='email address',
        unique=True,
    )


__all__ = (
    'User',
)
