from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import User, OTP
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.utils import timezone



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
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username_or_email', 'password', 'access_token', 'refresh_token']

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        # پیدا کردن کاربر با نام کاربری یا ایمیل
        user = (User.objects.filter(username=username_or_email).first() or
                User.objects.filter(email=username_or_email).first())

        if not user:
            raise AuthenticationFailed('User not found.')

        if not user.is_verified:
            raise AuthenticationFailed('User not verified.')

        # احراز هویت با استفاده از نام کاربری و رمز عبور
        authenticated_user = authenticate(username=username_or_email, password=password)
        if not authenticated_user:
            raise AuthenticationFailed('Invalid credentials, try again.')

        # ایجاد و ارسال توکن‌های دسترسی و تجدید
        refresh = RefreshToken.for_user(authenticated_user)
        return {
            'username_or_email': authenticated_user.username,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

# اگر نیاز به سریالایزر برای پروفایل دارید، به این صورت می‌توانید آن را تعریف کنید:
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'
