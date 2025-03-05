import random
from django.views import View
from rest_framework.generics import GenericAPIView
from .models import OTP, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .email import send_otp_email
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.views.generic import TemplateView


class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  # ذخیره کاربر در پایگاه داده
            send_otp_email(user.email)  # ارسال کد OTP به ایمیل
            return Response({
                'message': f'Hi {user.username}, thanks for signing up. A passcode has been sent to your email.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(GenericAPIView):
    def post(self, request):
        otpcode = request.data.get('otp')
        email = request.data.get('email')

        try:
            # یافتن OTP برای تایید
            user_code_obj = OTP.objects.get(otp=otpcode, user__email=email)
            user = user_code_obj.user

            # اگر کاربر تایید نشده باشد، وضعیت is_verified را True می‌کنیم
            if not user.is_verified:
                user.is_verified = True
                user.save()  # تغییر وضعیت به True

                # ورود کاربر بعد از تایید
                login(request, user)
                return Response({
                    'message': 'Account email verified successfully, and you are now logged in.'
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'Code is invalid, user already verified'
            }, status=status.HTTP_204_NO_CONTENT)

        except OTP.DoesNotExist:
            return Response({
                'message': 'Invalid OTP or OTP not found'
            }, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # بررسی وضعیت تایید کاربر قبل از ورود
        user = serializer.validated_data['user']
        if not user.is_verified:
            return Response({
                'message': 'Your email is not verified. Please verify your email first.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # ورود کاربر پس از تایید
        login(request, user)
        return Response({
            'message': 'Login successful.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)

class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class HomeView(TemplateView):
    template_name = "home.html"

# class LoginView(TemplateView):
#      template_name = "login.html"

# class SignupView(TemplateView):
#      template_name = "signup"


class ProfileView(TemplateView):
    template_name = "profile.html"

# class OTPView(TemplateView):
#     template_name = "otp.html"
