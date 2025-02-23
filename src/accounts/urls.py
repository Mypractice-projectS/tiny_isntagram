from django.urls import path
from .views import HomeView, LoginView, SignUpView, ProfileView, OTPView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('otp/', OTPView.as_view(), name='otp'),
]
