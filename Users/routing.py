from django.urls import re_path
from . import consumers

users_websocket_urlpatterns = [
    re_path(r"ws/user/(?P<uuid>\w+)/$", consumers.UserConsumer.as_asgi()),
]