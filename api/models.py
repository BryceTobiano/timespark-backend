from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime
from django.utils.timezone import now


# Custom User Model
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
    """
    Custom user class replacing email for username
    """
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    googleSignUpOnly = models.BooleanField(default=False)

    google_access_token = models.TextField(max_length=255, default="")
    google_refresh_token = models.TextField(max_length=255, default="")
    token_expiry = models.DateTimeField(default=now())

    username = None
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Category(models.Model):
    """
    Represents a category of events created by a specific user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete all categories if the user is deleted
        related_name='event_categories'  # Access categories with user.event_categories.all()
    )
    name = models.CharField(max_length=100, help_text="Name of the category")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the category")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']  # Categories are ordered by name by default
    
    def __str__(self):
        return f"{self.name} (User: {self.user.username})"


class Calendar(models.Model):
    """
    A calendar that belongs to a user and contains events.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete the calendar if the user is deleted
        related_name='calendars'   # Allows reverse access: user.calendars.all()
    )
    name = models.CharField(max_length=100, help_text="Name of the calendar")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the calendar")
    default_category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,  # Set to NULL if the category is deleted
        null=True,  # Allow the calendar to exist without a default category
        blank=True,
        related_name='default_for_calendars',  # Allows reverse access from categories
        help_text="Default category for events in this calendar"
    )
    color = models.CharField(
        max_length=7,  # To accommodate hex color codes like #FFFFFF
        default='#000000',  # Default to black
        help_text="Color of the calendar in hex format (e.g., #FF5733)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"

class Event(models.Model):
    """
    An event in a calendar.
    """
    calendar = models.ForeignKey(
        Calendar,
        on_delete=models.CASCADE,  # Delete events if the calendar is deleted
        related_name='events'      # Allows reverse access: calendar.events.all()
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete events if the user is deleted
        related_name='events',     # Allows reverse access: user.events.all()
        help_text="The user who created or owns this event"
    )
    title = models.CharField(max_length=200, help_text="Title of the event")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the event")
    start = models.DateTimeField(help_text="Event start time")
    end = models.DateTimeField(help_text="Event end time")
    allDay = models.BooleanField(default=False, help_text="Is this an all-day event?")
    categories = models.ManyToManyField(
        Category,
        related_name='events',  # Access events by category.events.all()
        blank=True  # Allow events to have no categories
    )
    color = models.CharField(
        max_length=7,  # To accommodate hex color codes like #FFFFFF
        default='#000000',  # Default to black
        help_text="Color of the calendar in hex format (e.g., #FF5733)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (Calendar: {self.calendar.name})"
    
