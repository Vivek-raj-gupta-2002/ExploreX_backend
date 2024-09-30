from django.urls import path, re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),  # Use as_asgi() for async consumers
]
