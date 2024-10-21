import json
from openai import AzureOpenAI
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chatApp.models import Chat, Message, AIMessages
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import google.generativeai as genai

# Configure Bard API with the provided API key
genai.configure(api_key=settings.BARD_API)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handles the WebSocket connection. Authenticates the user, sets up the AI client,
        and adds the user to the appropriate chat group.
        """
        # Retrieve JWT token from query string
        token = self.scope['query_string'].decode().split('=')[1]
        
        # Authenticate the user using the JWT token
        self.user = await self.authenticate_token(token)
        if self.user is None:
            # If authentication fails, close the connection
            await self.close()
            return

        self.scope['user'] = self.user
        self.chat_id = self.scope['url_route']['kwargs']['room_name']


        # Base prompt for OpenAI
        self.base_prompt = (
            "You are a kind, empathetic, and attentive mental health assistant. "
            "Your role is to offer emotional support and coping strategies to help users."
        )

        # Base prompt for Bard AI
        self.bard_base_prompt = (
            "You are a friendly assistant providing warm, empathetic support "
            "for mental health issues. Respond concisely and clearly with empathy."
            "Your responce should be just raw answer without Responce tag"
            "use multiple life related books like Bhagwat gita and all to understand and solve problems of user"
        )

        # If the chat room is an AI-generated room, generate the unique AI room ID
        if "AI" in self.chat_id:
            self.chat_id = await self.generate_user_ai_room_id(self.user)

        # Create a group name based on chat ID
        self.chat_group_name = f'chat_{self.chat_id}'
        
        # Add the user to the chat group
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles the WebSocket disconnection. Removes the user from the chat group.
        """

        pass
        if hasattr(self, 'chat_group_name'):
            await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handles receiving messages via WebSocket. Broadcasts the message to the group,
        processes AI responses if needed, and saves the message to the database.
        """
        data = json.loads(text_data)
        message_content = data.get('message')
        sender_username = self.scope['user'].username

        # Send the message to the group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': sender_username
            }
        )

        # If it's an AI chat, call the Bard AI to get a response
        if self.chat_id.startswith("AI_"):
            reply = await self.bard_ai(message_content)
            # Send AI response to the group
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'message': reply,
                    'sender': 'AI'
                }
            )
            # Save the AI conversation to the database
            await self.save_ai_message(sender_username, message_content, reply)
        else:
            # Save regular user messages to the database
            await self.save_message(sender_username, message_content)

    async def chat_message(self, event):
        """
        Handles broadcasting messages to all users in the chat group.
        """
        message = event['message']
        sender = event['sender']

        # Send the message to the WebSocket client
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @sync_to_async
    def save_message(self, sender_username, message_content):
        """
        Saves a regular user message to the database.
        """
        sender = User.objects.get(username=sender_username)
        chat = Chat.objects.get(id=self.chat_id)
        Message.objects.create(chat=chat, sender=sender, content=message_content)

    @sync_to_async
    def authenticate_token(self, token):
        """
        Authenticates the JWT token and retrieves the associated user.
        """
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(token)
            return jwt_authenticator.get_user(validated_token)
        except (InvalidToken, TokenError):
            return None

    @sync_to_async
    def save_ai_message(self, sender_username, message_content, reply):
        """
        Saves AI-generated messages and user input to the database.
        """
        sender = User.objects.get(username=sender_username)
        AIMessages.objects.create(user=sender, message=message_content, reply=reply)

    @sync_to_async
    def call_chatgpt(self, prompt):
        """
        Calls OpenAI's GPT API to get a response for the provided prompt.
        """
        # print(settings.OPENAI_API_KEY, type(settings.OPENAI_API_KEY))
        try:
            
            client = AzureOpenAI(
                api_key=settings.OPENAI_API_KEY,
                api_version=settings.API_VERSION,
                azure_endpoint=settings.ENDPOINT
            )

            chat_history = self.get_AI_history()
            history = "\n".join([f"User: {m.message}\nAI: {m.reply}" for m in chat_history])
            
            # Create a combined prompt with the history and user input
            combined_prompt = (
                f"Basic Prompt: {self.bard_base_prompt}\n"
                f"History:\n{history}\n"
                f"New Message: {prompt}"
            )
            
            response = client.completions.create(
                model=settings.MODEL,
                prompt=combined_prompt,
                max_tokens=20,
                # stream=True,
            )

            return response.choices[0].text.strip()
        except Exception as e:
            print(f'Error calling OpenAI API: {str(e)}')
            return "Sorry, I couldn't process that."

    @sync_to_async
    def generate_user_ai_room_id(self, user):
        """
        Generates a unique AI room ID based on the user's ID.
        """
        return f"AI_{user.id}"

    @sync_to_async
    def bard_ai(self, prompt):
        """
        Calls Bard AI's API to get a response based on the user prompt and chat history.
        """
        try:
            # Get chat history for context
            chat_history = self.get_AI_history()
            history = "\n".join([f"User: {m.message}\nAI: {m.reply}" for m in chat_history])
            
            # Create a combined prompt with the history and user input
            combined_prompt = (
                f"Basic Prompt: {self.bard_base_prompt}\n"
                f"History:\n{history}\n"
                f"New Message: {prompt}"
            )
            
            # Call Bard AI to generate a response
            response = genai.GenerativeModel("gemini-1.5-pro").generate_content(combined_prompt)
            
            return response.text
        except Exception as e:
            print(f'Error calling Bard API: {str(e)}')
            return "Sorry, I couldn't process that."

    def get_AI_history(self):
        """
        Retrieves the last 10 AI-generated messages for the user to provide context.
        """
        return AIMessages.objects.filter(user=self.user).order_by('-timestamp')[:10]
