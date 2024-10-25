from django.db import models
from django.conf import settings

# Create your models here.
class UserSummary(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='summary')
    date = models.DateField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    task = models.TextField(null=True, blank=True)
    personality = models.TextField(null=True, blank=True)
    mood = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} on {self.date}'
    
    class Meta:
        unique_together = ('user', 'date')