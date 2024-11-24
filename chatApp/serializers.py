# serializers.py
from rest_framework import serializers
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    undelivered_message_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['title', 'last_message', 'id', 'undelivered_message_count']

    def get_last_message(self, obj):
        return obj.messages.last().content if obj.messages.exists() else None

    def get_undelivered_message_count(self, obj):
        # Get the user making the request
        request = self.context.get('request')
        if not request or not request.user:
            return 0

        # Count messages in this chat that are not sent by the user and have status 'sent'
        return obj.messages.filter(status='sent').exclude(sender=request.user).count()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'status']
