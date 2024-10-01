import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chatApp.models import Chat, Message  # Import the Chat and Message models
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the token from the query params
        token = self.scope['query_string'].decode().split('=')[1]

        # Authenticate the user with JWT token
        user = await self.authenticate_token(token)
        if user is None:
            await self.close()
            return

        # Set the authenticated user in the scope
        self.scope['user'] = user

        # Retrieve chat_id from URL parameters
        self.chat_id = self.scope['url_route']['kwargs']['room_name']  
        self.chat_group_name = f'chat_{self.chat_id}'

        # Add user to the chat group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Check if chat_group_name is defined
        if hasattr(self, 'chat_group_name'):
            # Remove user from the chat group if the group name exists
            await self.channel_layer.group_discard(
                self.chat_group_name,
                self.channel_name
            )


    async def receive(self, text_data):
        # Load incoming message data
        data = json.loads(text_data)
        message_content = data.get('message')  # Use .get() for safety
        sender_username = self.scope['user'].username  # Ensure the user is authenticated
        
        # Save message to the database
        await self.save_message(sender_username, message_content)

        # Broadcast message to the group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': sender_username
            }
        )

    async def chat_message(self, event):
        # Extract the message and sender from the event
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @sync_to_async
    def save_message(self, sender_username, message_content):
        # Get the sender user object
        sender = User.objects.get(username=sender_username)
        # Get the Chat instance
        chat = Chat.objects.get(id=self.chat_id)
        # Save the message
        Message.objects.create(chat=chat, sender=sender, content=message_content)

    @sync_to_async
    def authenticate_token(self, token):
        """
        Authenticate the JWT token and return the user if valid.
        """
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(token)
            # Get the user from the token
            return jwt_authenticator.get_user(validated_token)
        except (InvalidToken, TokenError) as e:
            print(f"Token authentication failed: {str(e)}")
            return None
