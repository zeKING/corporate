from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/<int:from_id>/<int:to_id>', consumers.ChatConsumer.as_asgi()),
]