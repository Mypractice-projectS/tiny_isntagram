from tempfile import template
from django.urls import path
from . import views
from django.contrib.auth.views import  PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.authtoken import views as auth_token
from django.views.generic import TemplateView

urlpatterns = [
    #home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # register
    path('api/signup/', views.UserRegisterView.as_view(), name='signup-api'),
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),
    path('verify_otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    #login
    path('api/login/', views.UserLoginView.as_view(), name='login-api'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    # logout
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    # profile
    path('api/profile/', views.ProfileView.as_view(), name='profile-api'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('profile/<int:profile_pk>/', views.ProfileView.as_view(), name='profile_get'),
    # TOKEN JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]