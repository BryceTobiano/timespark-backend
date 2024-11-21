from django.contrib import admin
from django.urls import path,include
from .views import index, CreateUserView, ListUsersView, GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('/', CreateUserView, name="HelloWorld"),
    path('register/', CreateUserView.as_view(), name="register"),
    path('users/', ListUsersView.as_view(), name="users"),
    path('google/auth', GoogleCalendarInitView.as_view(), name="google"),
    path('google/redirect', GoogleCalendarRedirectView.as_view(), name="google"),
]
