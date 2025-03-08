from typing import Generic
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from permissions import IsOwnerOrReadOnly
from .models import User, Profile ,OTP
from .email import send_otp_email
from .serializers import UserRegisterSerializer, UserLoginSerializer, ProfileSerializer, UserUpdateSerializer,LogoutUserSerializer
# from django.contrib.auth import login
# from django.utils import timezone
# from datetime import timedelta



class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_otp_email(user['email'])
            print(user)
            # send email
            return Response({
                'data':user,
                'message':f'hi {user} thanks for signing up a passcode'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(GenericAPIView):
    def post(self, request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = OTP.objects.get(otp=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message':'account email verified successfully'
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'code is invalid user already verified'
            }, status=status.HTTP_204_NO_CONTENT)

        except OTP.DoesNotExist:
            return Response({
                'message': 'passcode not provided'
            }, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class ProfileView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def get(self, request,profile_pk):
        try:
            profile = Profile.objects.get(pk=profile_pk, user=request.user)
            self.check_object_permissions(request, profile)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
