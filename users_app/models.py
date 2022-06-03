from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('User must provide email.')
        if not first_name:
            raise ValueError('User must provide first name.')
        if not last_name:
            raise ValueError('User must provide last name.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_email_verified = True
        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, unique=False, verbose_name='first name')
    last_name = models.CharField(max_length=30, unique=False, verbose_name='last name')
    email = models.EmailField(max_length=100, unique=True, verbose_name='email')
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email
