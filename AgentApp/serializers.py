from rest_framework import serializers
from .models import UserSummary

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSummary
        fields = ['date', 'summary', 'task', 'personality', 'mood']
