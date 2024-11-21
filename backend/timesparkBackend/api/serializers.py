from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email

        return token
    
    def validate(self, attrs):
        # Override validate to authenticate with the correct username_field
        request_data = self.context.get('request').data
        username = request_data.get('email')  # Match the field you're using
        password = request_data.get('password')

        if username and password:
            # user =  User.objects.filter(email=username).first() # TODO: Use authenticate() method instead
            user = authenticate(email=username, password=password)

            if user is None: 
                raise AuthenticationFailed('User not found!')

        else:
            raise serializers.ValidationError('Email and password are required')

        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }