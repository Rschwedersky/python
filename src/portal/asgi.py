"""
ASGI config for portal project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from django.core.asgi import get_asgi_application

from my_solutions.consumers import TasksConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/models/state/$',
                TasksConsumer.as_asgi()),
        ]),
    ),
})
