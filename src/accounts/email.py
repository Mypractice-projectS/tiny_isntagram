from django.core.mail import send_mail,EmailMessage
import random
from .models import User,OTP
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email):
    subject = 'Your OTP'
    otp_code = generate_otp()
    print(otp_code)
    user = User.objects.filter(email=email).first()
    if not user:
        print("User not found with this email.")
        return

    # current_site='tinyinstagramserver@gmail.com'
    email_body=f'Hi {user} thanks for signing up on Tiny instagram please verify your email with the \n one time passcode {otp_code}'
    from_email = settings.EMAIL_HOST_USER


    OTP.objects.create(user=user,otp=otp_code)

    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_email.send(fail_silently=False)
    print("Email sent successfully.")

def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']],
    )
    email.send(fail_silently=False)
    print("Normal email sent successfully.")