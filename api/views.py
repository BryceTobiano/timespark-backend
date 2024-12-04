# DRF Imports
from django.shortcuts import get_object_or_404, render
from .models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .utils import get_user_id_from_token

# Google Calendar Imports
import os
from django.shortcuts import redirect
from django.views import View
from google_auth_oauthlib.flow import Flow
import requests
from django.utils.timezone import now
from django.db import IntegrityError
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# View users, for debugging 
class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class MyTokenObtainPairView(TokenObtainPairView):
    queryset = User.objects.all()
    serializer_class = MyTokenObtainPairSerializer

REDIRECT_URI = 'http://127.0.0.1:8000/api/google/redirect'
# Set up OAuth2 scope and flow
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
flow = Flow.from_client_config(
    client_config={
        'installed': {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uris': [REDIRECT_URI],
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://accounts.google.com/o/oauth2/token',
        }
    },
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI,
)

class GoogleCalendarInitView(View):
    def get(self, request):
        # Generate authorization URL and redirect user to Google authorization page
        authorization_url, _ = flow.authorization_url(prompt='consent')
        return redirect(authorization_url)
    
class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Get authorization code from query parameters
        code = request.GET.get('code')
        # Exchange authorization code for access token
        flow.fetch_token(code=code)
        credentials = flow.credentials

        print(credentials.expiry - now())

        # Retrieve the user's email from the id_token or userinfo endpoint
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {credentials.token}"}
        )
        
        user_info = None
        if response.status_code == 200:
            user_info = response.json()
            print(user_info)

        response = HttpResponseRedirect('http://127.0.0.1:3000/dashboard')
        try:
            user, created = User.objects.update_or_create(
                email = user_info.get('email'),

                defaults={
                    'name': user_info.get('name'),
                    'google_access_token': credentials.token,
                    'google_refresh_token': credentials.refresh_token,
                    'token_expiry': now() + (credentials.expiry - now())
                }
            )
            
            if created:
                user.googleSignUpOnly = True
            
            refresh = RefreshToken.for_user(user)
            response.set_cookie('timesparkRefreshToken', str(refresh))
            response.set_cookie('timesparkAccessToken', str(refresh.access_token))
        except IntegrityError as e:
            print("Integrity Error:", e)

        return response

from .models import Calendar, Event, Category, Task
from .serializers import CalendarSerializer, EventSerializer, CategorySerializer, TaskSerializer

class CalendarListCreateView(generics.ListCreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    permission_classes = [AllowAny] #TODO: Delete this line

    def get_queryset(self):
        """
        Optionally filters the calendars by 'user' query parameter.
        """
        queryset = Calendar.objects.all()
        user_id = self.request.query_params.get('user')  # Fetch the 'user' query parameter
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny] #TODO: Delete this line

    def get_queryset(self):
        """
        Optionally filters the calendars by 'user' query parameter.
        """
        queryset = Event.objects.all()
        user_id = self.request.query_params.get('user')  # Fetch the 'user' query parameter
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    

class EventsDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny] #TODO: Delete this line
    lookup_field = "id"

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] #TODO: Delete this line

    def get_queryset(self):
        """
        Optionally filters the calendars by 'user' query parameter.
        """
        queryset = Category.objects.all()
        user_id = self.request.query_params.get('user')  # Fetch the 'user' query parameter
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny] #TODO: Delete this line

    def get_queryset(self):
        """
        Optionally filters the calendars by 'user' query parameter.
        """
        queryset = Task.objects.all()
        user_id = self.request.query_params.get('user')  # Fetch the 'user' query parameter
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class UserDashboardView(APIView):
    permission_classes = [AllowAny]   #TODO: Delete this line

    def get(self, request, user_id=None):
        user = request.user if user_id is None else User.objects.get(id=user_id)

        # Get the user's calendars, events, and categories
        calendars = Calendar.objects.filter(user=user)
        events = Event.objects.filter(user=user)
        categories = Category.objects.filter(user=user)

        # Serialize the data
        calendar_data = CalendarSerializer(calendars, many=True).data
        event_data = EventSerializer(events, many=True).data
        category_data = CategorySerializer(categories, many=True).data

        # Return combined data
        return JsonResponse({
            'calendars': calendar_data,
            'events': event_data,
            'categories': category_data
        })
