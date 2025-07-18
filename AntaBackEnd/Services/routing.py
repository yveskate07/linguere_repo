from django.urls import re_path

from . import consumers

services_websocket_urlpatterns = [
    re_path(r"ws/service/(?P<service_name>\w+)/$", consumers.ServiceConsumer.as_asgi()),
]