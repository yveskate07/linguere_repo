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
from django.urls import path
from .views import arduino, machine, installations, verify_hmac, return_url, init_payment, cart_view, payment_done, \
    fetch_articles

urlpatterns = [
    path('arduino/<int:page>', arduino, name='shop-arduino'),
    path('machine/<int:page>', machine, name='shop-machine'),
    path('installations/<int:page>', installations, name='shop-installations'),
    path('fetch-articles/', fetch_articles, name='fetch-articles'),
    path('create-payment/', init_payment, name='create_payment'),
    path('notify/', verify_hmac, name='verify_hmac'),
    path('return/', return_url, name='return_url'),
    path('cart/', cart_view, name='cart'),
    path('payment-done/', payment_done, name='payment-done')
]
