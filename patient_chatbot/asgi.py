"""
ASGI config for patient_chatbot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patient_chatbot.settings")
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chatbot.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patient_chatbot.settings")
application = ProtocolTypeRouter({
    # HTTP goes to the Django ASGI app we just set up
    "http": django_asgi_app,

    # WebSocket connections get routed to your ChatConsumer
    "websocket": AuthMiddlewareStack(
        URLRouter(chatbot.routing.websocket_urlpatterns)
    ),
})