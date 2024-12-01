from django.contrib import admin
from django.urls import path,include
from .views import CreateUserView, ListUsersView, GoogleCalendarInitView, GoogleCalendarRedirectView
from .views import EventListCreateView, EventsDeleteView, CalendarListCreateView, CategoryListCreateView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name="register"),
    path('google/auth', GoogleCalendarInitView.as_view(), name="google-auth"),
    path('google/redirect', GoogleCalendarRedirectView.as_view(), name="google-redirect"),
    path('events/', EventListCreateView.as_view(), name="events"),
    path('events/<int:id>/', EventsDeleteView.as_view(), name="events"),
    path('calendar/', CalendarListCreateView.as_view(), name="calendars"),
    path('category/', CategoryListCreateView.as_view(), name="categories"),
    # TODO: Test URLS: Delete these URLs
    path('users/', ListUsersView.as_view(), name="users"), 
]
