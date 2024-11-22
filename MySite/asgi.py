import os
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MySite.settings')
django.setup()
application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chatApp import routing  # Import the routing from your chat app

application = ProtocolTypeRouter({
    'http': application,
    'websocket': AllowedHostsOriginValidator(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
