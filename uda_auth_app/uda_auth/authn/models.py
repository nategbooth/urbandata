from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomAuthUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates a user with the email, password, and other characteristics given.
        """
        if not email:
            raise ValueError("You must include an email address")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a user with the email, password, and other characteristics given.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomAuthUser(AbstractUser):
    # Make username not required
    username = None
    email = models.EmailField(verbose_name='email address', unique=True)
    company = models.TextField(max_length=500, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomAuthUserManager()


