from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def Sign_up(request):
    return render(request, "signup.html")
