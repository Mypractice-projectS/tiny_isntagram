from django.urls import path
from .views import home , login , Sign_up

urlpatterns = [
    path('', home, name='home'), 
    path('login', login, name='login'), 
    path('signup', Sign_up, name='sign-up'), 
]
