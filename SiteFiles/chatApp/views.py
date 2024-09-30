from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only fetch active chats where the user is a participant
        return Chat.objects.filter(participants=self.request.user, is_active=True)

    def destroy(self, request, *args, **kwargs):
        # Soft delete: mark chat as inactive instead of hard deletion
        chat = self.get_object()
        chat.is_active = False
        chat.save()
        return Response({'status': 'chat deleted'})

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat__id=chat_id).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, chat_id=self.kwargs['chat_id'])
