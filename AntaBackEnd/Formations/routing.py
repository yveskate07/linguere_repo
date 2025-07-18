from django.urls import re_path

from . import consumers

formations_websocket_urlpatterns = [
    re_path(r"ws/formation/(?P<formation_name>\w+)/$", consumers.FormationConsumer.as_asgi()),
]