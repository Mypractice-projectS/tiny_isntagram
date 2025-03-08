import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.urls import reverse
from rest_framework_simplejwt.exceptions import TokenError
from accounts.email import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken,Token
from accounts.models import User, Profile,OTP



class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, value):
        if value == 'password':
            raise serializers.ValidationError('Username cannot be "password".')
        return value

    def validate(self, data):

        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data





class UserLoginSerializer(serializers.ModelSerializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(max_length=255,read_only=True)
    refresh_token = serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = User
        fields = ['username_or_email','password','access_token','refresh_token']

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        user = (User.objects.filter(username=username_or_email).first() or
                User.objects.filter(email=username_or_email).first())

        if user and User.is_verified:
            authenticated_user = authenticate(username=username_or_email, password=password)
            if not authenticated_user:
                raise AuthenticationFailed('Invalid credentials try again.')
            user_tokens = user.tokens()


            return {
                'username_or_email': user.username,
                'access_token': str(user_tokens.get('access')),
                'refresh_token': str(user_tokens.get('refresh')),

            }

class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token':('Token is invalid or has expired.')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')









class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','phone']



class ProfileSerializer(serializers.ModelSerializer):
    # avatar = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('user', 'avatar', 'bio', 'first_name', 'last_name', 'age')
