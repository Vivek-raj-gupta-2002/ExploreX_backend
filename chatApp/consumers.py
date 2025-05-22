import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chatApp.models import Chat, Message, AIMessages
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import google.generativeai as genai
from openai import AzureOpenAI

# Configure Google Generative AI with API key
genai.configure(api_key=settings.BARD_API)

class ChatConsumer(AsyncWebsocketConsumer):
    bard_base_prompt = (
            "You are a kind, empathetic, and attentive mental health assistant. "
            "Your role is to offer emotional support and coping strategies to help users."
        )
    
    async def connect(self):
        # Authenticate user with JWT token
        token = self.scope['query_string'].decode().split('=')[1]
        self.user = await self.authenticate_token(token)
        if self.user is None:
            await self.close()
            return

        self.scope['user'] = self.user
        self.chat_title = self.scope['url_route']['kwargs']['room_name']

        # Generate a unique room title for AI chats
        if "AI" in self.chat_title:
            self.chat_title = await self.generate_user_ai_room_title(self.user)

        self.chat_group_name = f'chat_{self.chat_title}'

        # Join the WebSocket group for the chat
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

        # Send undelivered messages if this is a user-to-user chat
        if 'AI' not in self.chat_title:
            await self.send_undelivered_messages()

    async def disconnect(self, close_code):
        # Leave the chat group on disconnect
        if hasattr(self, 'chat_group_name'):
            await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        # Process incoming WebSocket messages
        data = json.loads(text_data)
        message_content = data.get('message')
        sender_username = self.scope['user'].username

        # Send message to the chat group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': sender_username
            }
        )

        # Process AI response if the chat title indicates an AI chat
        if self.chat_title.startswith("AI_"):
            reply = await self.bard_ai(message_content)
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
        # Send message to WebSocket
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    async def send_undelivered_messages(self):
        # Retrieve and send undelivered messages to the user
        undelivered_messages = await self.get_undelivered_messages()

        for message in undelivered_messages:
            await self.send(text_data=json.dumps(message))
            

    @sync_to_async
    def get_undelivered_messages(self):
        # Fetch messages that are marked as sent but undelivered
        data = Message.objects.filter(
            chat__id=self.chat_title,
            chat__participants=self.user,
            status='sent'
        ).exclude(sender=self.user)


        ans = []

        for mess in data:
            ans.append({'message': mess.content, 'sender': mess.sender.username,'time': mess.timestamp.strftime('%H:%M:%S')})
            mess.status = 'delivered'
            mess.save()
        
        return ans



    @sync_to_async
    def save_message(self, sender_username, message_content):
        # Save a new message to the database
        sender = User.objects.get(username=sender_username)
        chat = Chat.objects.get(id=self.chat_title)
        Message.objects.create(chat=chat, sender=sender, content=message_content)

    @sync_to_async
    def authenticate_token(self, token):
        # Authenticate the user using a JWT token
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(token)
            return jwt_authenticator.get_user(validated_token)
        except (InvalidToken, TokenError):
            return None

    @sync_to_async
    def save_ai_message(self, sender_username, message_content, reply):
        # Save AI-generated messages in the database
        sender = User.objects.get(username=sender_username)
        AIMessages.objects.create(user=sender, message=message_content, reply=reply)

    @sync_to_async
    def generate_user_ai_room_title(self, user):
        # Generate a unique room title for AI chats
        return f"AI_{user.id}"

    @sync_to_async
    def bard_ai(self, prompt):
        """
        Calls Bard AI's API to get a response based on the user prompt and chat history.
        """
        try:
            chat_history = self.get_AI_history()
            history = "\n".join([f"User: {m.message}\nAI: {m.reply}" for m in chat_history])
            
            # Create a combined prompt with the history and user input
            combined_prompt = (
                f"Basic Prompt: {self.bard_base_prompt}\n"
                f"History:\n{history}\n"
                f"New Message: {prompt}"
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. && also show positivity in every aspects"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling Azure OpenAI API: {str(e)}")
            return "Sorry, I couldn't process that."


        # try:
        #     # Get chat history for context
        #     chat_history = self.get_AI_history()
        #     history = "\n".join([f"User: {m.message}\nAI: {m.reply}" for m in chat_history])
            
        #     # Create a combined prompt with the history and user input
        #     combined_prompt = (
        #         f"Basic Prompt: {self.bard_base_prompt}\n"
        #         f"History:\n{history}\n"
        #         f"New Message: {prompt}"
        #     )
            
        #     # Call Bard AI to generate a response
        #     response = genai.GenerativeModel("gemini-1.5-pro").generate_content(combined_prompt)
            
        #     return response.text
        
        # except Exception as e:
        #     print(f'Error calling Bard API: {str(e)}')
        #     return "Sorry, I couldn't process that."

    
    def get_AI_history(self):
        # Retrieve recent AI chat history
        return AIMessages.objects.filter(user=self.user).order_by('-timestamp')[:10]
