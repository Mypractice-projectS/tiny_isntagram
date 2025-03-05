from django.views.generic import TemplateView
from django.urls import path
from .views import HomeView, UserRegisterView, ProfileView, OTPView,UserLoginView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('api/login/', UserRegisterView.as_view(), name='login-api'),
    path('api/signup/', UserRegisterView.as_view(), name='user-register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('otp/', OTPView.as_view(), name='otp'),
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),

]
