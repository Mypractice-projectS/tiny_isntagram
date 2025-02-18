
from django.db import models
from accounts.models import Profile

class Story(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField()
    likes = models.BigIntegerField(default=0)
    reply = models.BigIntegerField(default=0)
    
    