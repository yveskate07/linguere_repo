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
from .views import arduino, machine, installations, verify_hmac, return_url, init_payment

# urlpatterns = [
#     path('arduino/<int:page_number>', arduino, name='shop-arduino'),
#     path('machine/<int:page_number>', machine, name='shop-machine'),
#     path('installations/<int:page_number>', installations, name='shop-installations'),
#     path('notify/', verify_hmac, name='verify_hmac'),
#     path('return/', return_url, name='return_url')
# ]
urlpatterns = [
    path('arduino/', arduino, name='shop-arduino'),
    path('machine/', machine, name='shop-machine'),
    path('installations/', installations, name='shop-installations'),
    path('create-payment/', init_payment, name='create_payment'),
    path('notify/', verify_hmac, name='verify_hmac'),
    path('return/', return_url, name='return_url')
]
