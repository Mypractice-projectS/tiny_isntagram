from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request, "home.html")

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

class SignUpView(View):
    def get(self, request):
        return render(request, "signup.html")

class ProfileView(View):
    def get(self, request):
        return render(request, "profile.html")

class OTPView(View):
    def get(self, request):
        return render(request, "otp.html")

class OTPView(View):
    def get(self, request):
        return render(request, "otp.html")
