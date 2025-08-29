# products/routing.py

from django.urls import re_path
from . import consumers

shop_websocket_urlpatterns = [
    re_path(r'^ws/shop/user(?:/(?P<uuid>[A-Za-z0-9]+))?/$',consumers.ProductConsumerAuth.as_asgi())]
