from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views  # از اینجا به بعد می‌توانید فقط از `views` استفاده کنید


urlpatterns = [
    # صفحه خانه
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # ثبت‌نام
    path('api/signup/',views.UserRegisterView.as_view(), name="api_signup"),
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),
    path('verify/otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('otp/', TemplateView.as_view(template_name='otp.html'), name='otp'),

    # ورود و خروج
    path('api/login/', views.UserLoginView.as_view(), name='api_login'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    
    # به‌روزرسانی پروفایل
    path('update/<int:user_pk>/', views.UserUpdateView.as_view(), name='user_update'),

    # تغییر رمز عبور
    path('password_reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('set_new_password/', views.SetNewPasswordView.as_view(), name='set_new_password'),

    # پروفایل
    path('creatprofile/', TemplateView.as_view(template_name='creat_profile.html'), name='creat_profile'),
    path('api/profile/<int:id>/', views.ProfileView.as_view(), name='api_profile'),
    path('profile/<int:id>/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    # path('profile/<int:id>/', views.ProfileView.as_view(), name='profile_get'),
    path('profile_update/<int:profile_pk>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile_delete/<int:profile_pk>/', views.ProfileDeleteView.as_view(), name='profile_delete'),

    # توکن JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
