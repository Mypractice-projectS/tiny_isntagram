from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from permissions import IsOwnerOrReadOnly
from .models import User, OTP,Profile
from .serializers import (UserRegisterSerializer, UserLoginSerializer, 
                        ProfileSerializer, PasswordResetRequestSerializer, 
                        SetNewPasswordSerializer,LogoutUserSerializer,VerifyOTPSerializer)
from .email import send_otp_email


class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_data = serializer.data
            send_otp_email(user.email)
            print(user)
            # send email
            return Response({
                'data':user_data,
                'message':f'hi {user_data['email']} thanks for signing up a passcode'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(GenericAPIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otpcode = serializer.validated_data['otp']
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

#             Password

class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'a link has been sent to your email to reset your password'}, status=status.HTTP_200_OK)


class PasswordResetConfirm(GenericAPIView):
    def get(self, request,uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True,'message':'credentials is valid','uidb64':uidb64,'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'password reset successfull'},status=status.HTTP_200_OK)


#      logout

class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



#  <<<<<<<<<<<<<<  User Update  >>>>>>>>>>>>>>>>>>>

class UserUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def put(self, request,user_pk):
        user = User.objects.get(pk=user_pk,user=request.user)
        self.check_object_permissions(request, user)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# <<<<<<<<<<<<<<<<  end user update >>>>>>>>>>>>>>>>>>>>>>>



#    <<<<<<<<<<<<<<<<<<<   Profile  >>>>>>>>>>>>>>>>>>>>>>
#                    get post put delete


class ProfileView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, id=None):  # تغییر از profile_pk به id
        try:
            # استفاده از id برای پیدا کردن پروفایل
            profile = Profile.objects.get(pk=id, user=request.user)
            self.check_object_permissions(request, profile)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        try:
            existing_profile = Profile.objects.get(user=request.user)
            return Response({"detail": "Profile already exists. You can edit your profile."}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            serializer = ProfileSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                profile = serializer.save(user=request.user)
                return Response(ProfileSerializer(profile, context={'request': request}).data, status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        try:
            profile = Profile.objects.get(pk=id, user=request.user)
            self.check_object_permissions(request, profile)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# <<<<<<<<<<<<<<<<  update >>>>>>>>>>>>>>>>>>>>>>>

class ProfileUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def put(self, request, profile_pk):
        profile = Profile.objects.get(pk=profile_pk, user=request.user)
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# <<<<<<<<<<<<<<<<  delete >>>>>>>>>>>>>>>>>>>>>>>

class ProfileDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]
    def delete(self, request, profile_pk):
        profile = Profile.objects.get(pk=profile_pk, user=request.user)
        self.check_object_permissions(request, profile)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)