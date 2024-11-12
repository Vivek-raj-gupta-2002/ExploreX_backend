from django.db import models
from django.contrib.auth.models import User

class AIMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat b/w {self.user.username} and AI"

class Chat(models.Model):
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(User)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat between {', '.join(user.username for user in self.participants.all())}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('delivered', 'Delivered')], default='sent')

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat.id}"
