"""
ASGI config for AntaBackEnd project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AntaBackEnd.settings')
django.setup()

from Shop.routing import shop_websocket_urlpatterns
from Formations.routing import formations_websocket_urlpatterns
from Services.routing import services_websocket_urlpatterns
from Users.routing import users_websocket_urlpatterns

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(formations_websocket_urlpatterns + services_websocket_urlpatterns + users_websocket_urlpatterns + shop_websocket_urlpatterns))
        ),
    }
)