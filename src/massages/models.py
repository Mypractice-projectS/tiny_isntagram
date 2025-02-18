from django.db import models
from accounts.models import User

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    reply_id = models.BigIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    