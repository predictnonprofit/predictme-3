from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from data_handler.consumers import RunModelConsumer

websocket_url_pattern = [
    path("dashboard/data/ws/run-model", RunModelConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter(websocket_url_pattern))
})