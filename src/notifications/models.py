from django.db import models
from accounts.models import Profile

class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

