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
from .views import activate, login_user, register_user, user_home, user_edit, user_orders, user_favourites, user_tracked_deliveries

# path('favourites/', user_favourites, name='user_favourites'), path('tracked_deliveries/', user_tracked_deliveries, name='user_tracked_deliveries'),

urlpatterns = [
    path('', user_home, name='user_home'),
    path('edit/', user_edit, name='user_edit'),
    path('orders/', user_orders, name='user_orders'),
    path('login-user/', login_user, name='login-user'),
    path('register-user/', register_user, name='register-user'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
