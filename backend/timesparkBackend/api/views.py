# DRF Imports
from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

# Google Calendar Imports
import os
from dotenv import load_dotenv
from django.shortcuts import redirect
from django.views import View
from google_auth_oauthlib.flow import Flow
import requests
from django.utils.timezone import now
from django.db import IntegrityError



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
        except IntegrityError as e:
            print("Integrity Error:", e)

        return redirect('http://127.0.0.1:3000/dashboard')
