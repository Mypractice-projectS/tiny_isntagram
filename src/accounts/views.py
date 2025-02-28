from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView
from .serializers import UserRegisterSerializer



class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # send_otp_email(user.email, user.otp)  
            return Response({'message': ' OTP sent to email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HomeView(TemplateView):
    template_name = "home.html"

class LoginView(TemplateView):
     template_name = "login.html"

# class SignupView(TemplateView):
#     template_name = "signup"


class ProfileView(TemplateView):
    template_name = "profile.html"

class OTPView(TemplateView):
    template_name = "otp.html"
