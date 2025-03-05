import random  # برای تولید کد تصادفی OTP
from django.core.mail import EmailMessage  # برای ارسال ایمیل
from django.conf import settings  # برای دریافت تنظیمات ایمیل
from .models import User, OTP  # برای دسترسی به مدل‌های User و OTP



def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email):
    subject = 'Your OTP'
    otp_code = generate_otp()
    print(otp_code)
    user = User.objects.get(email=email)
    current_site='mohammadrezajavaherykian@gmail.com'
    email_body=f'Hi {user} thanks for signing up on {current_site} please verify your email with the \n one time passcode {otp_code}'
    from_email =settings.DEFAULT_FROM_EMAIL

    OTP.objects.create(user=user,otp=otp_code)

    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_email.send(fail_silently=True)
