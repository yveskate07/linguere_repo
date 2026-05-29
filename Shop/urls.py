"""
URL configuration for AntaBackEnd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from .views import arduino, machine, installations, verify_hmac, return_url, init_payment, cart_view, payment_done, \
    add_item, del_item, change_item

urlpatterns = [
    path('arduino/<int:page>', arduino, name='shop-arduino'),
    path('machine/<int:page>', machine, name='shop-machine'),
    path('installations/<int:page>', installations, name='shop-installations'),
    path('create-payment/', init_payment, name='create_payment'),
    path('notify/', verify_hmac, name='verify_hmac'),
    path('return/', return_url, name='return_url'),
    path('cart/', cart_view, name='cart'),
    path('add_item/', add_item, name='add_item'),
    path('del_item/', del_item, name='del_item'),
    path('change_item/', change_item, name='del_item'),
    path('payment-done/', payment_done, name='payment-done')
]


if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    # Configuration classique pour le développement local
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)