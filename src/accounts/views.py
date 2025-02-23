from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home.html"

class LoginView(TemplateView):
    template_name = "login.html"

class SignUpView(TemplateView):
    template_name = "signup.html"

class ProfileView(TemplateView):
    template_name = "profile.html"

class OTPView(TemplateView):
    template_name = "otp.html"
