from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set.')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(max_length=255, null=True, blank=True, verbose_name="email")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    employee_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    is_staff = models.BooleanField(default=False, verbose_name="is_staff")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
   

    def __str__(self):
        return self.username