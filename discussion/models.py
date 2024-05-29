from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Discussion(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_discussions')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_discussions')

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    read_time = models.DateTimeField(null=True, blank=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} in {self.discussion.title} - {self.content}"


