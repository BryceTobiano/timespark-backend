from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
        
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
 
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)  # change password to hash
        print("created new user using user manager");
        user.is_admin = False
        user.is_staff = False
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

