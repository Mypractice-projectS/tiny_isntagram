from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OTPViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'otps', OTPViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)), 
]
