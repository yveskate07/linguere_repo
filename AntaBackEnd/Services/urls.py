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
from .views import broderie, CNC, laser, serviceView

urlpatterns = [
    path('<str:service_name>/' , serviceView, name="serviceView"),
    path('CNC/' , CNC, name="services-cnc"),
    path('laser/' , laser, name="services-laser"),
    path('broderie/' , broderie, name="services-broderie"),
]
