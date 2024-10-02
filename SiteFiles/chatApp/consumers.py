import json
import openai
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chatApp.models import Chat, Message, AIMessages
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the token from the query params
        token = self.scope['query_string'].decode().split('=')[1]

        # Authenticate the user with JWT token
        user = await self.authenticate_token(token)
        if user is None:
            await self.close()
            return

        self.scope['user'] = user
        self.chat_id = self.scope['url_route']['kwargs']['room_name']

        # Generate unique AI chat room ID
        if "AI" in self.chat_id:
            self.chat_id = await self.generate_user_ai_room_id(user)
        
        self.chat_group_name = f'chat_{self.chat_id}'

        # Add user to the chat group
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'chat_group_name'):
            await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message')
        sender_username = self.scope['user'].username

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': sender_username
            }
        )

        # Save AI message and reply
        if self.chat_id.startswith("AI_"):
            reply = await self.call_chatgpt(message_content)
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'message': reply,
                    'sender': 'AI'
                }
            )
            await self.save_ai_message(sender_username, message_content, reply)
        else:
            await self.save_message(sender_username, message_content)

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @sync_to_async
    def save_message(self, sender_username, message_content):
        sender = User.objects.get(username=sender_username)
        chat = Chat.objects.get(id=self.chat_id)
        Message.objects.create(chat=chat, sender=sender, content=message_content)

    @sync_to_async
    def authenticate_token(self, token):
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(token)
            return jwt_authenticator.get_user(validated_token)
        except (InvalidToken, TokenError):
            return None

    @sync_to_async
    def save_ai_message(self, sender_username, message_content, reply):
        sender = User.objects.get(username=sender_username)
        AIMessages.objects.create(user=sender, message=message_content, reply=reply)

    @sync_to_async
    def call_chatgpt(self, prompt):
        """Call the OpenAI API to get a response from ChatGPT."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f'Error calling OpenAI API: {str(e)}')
            return "Sorry, I couldn't process that."

    @sync_to_async
    def generate_user_ai_room_id(self, user):
        """Generate a unique AI room ID using the user's unique identifier."""
        user = User.objects.get(email=user)
        return f"AI_{user.id}"
