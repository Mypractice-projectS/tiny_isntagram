from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from .managers import UserManager   
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,verbose_name="Email")
    username = models.CharField(max_length=50, unique=True, verbose_name="Username")
    phone_regex = RegexValidator(regex=r'^(0|0098|\+98)?9(0[1-5]|[1-3]\d|2[0-2]|9[0-9])\d{7}$',
                                 message='The entered phone number format is incorrect.')
    phone = models.CharField(validators=[phone_regex], max_length=11, blank=True, verbose_name="Phone number")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}, ( {self.username} )'


#   OTP

class OTP(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    otp = models.CharField(max_length=6, verbose_name="OTP Code")
    expires_at = models.DateTimeField(verbose_name="Expires at")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}, ( {self.otp} ),{self.created_at}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    bio = models.TextField()
    profile_img = models.ImageField(upload_to='images/', null=True, blank=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    