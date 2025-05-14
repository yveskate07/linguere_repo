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
from .views import impression_num_proposees, broderie_numerique, fraiseuse_numerique, decoupe_laser, impression_3D, \
    save_broderie_order

urlpatterns = [
    path('impression-3d/' , impression_3D, name="service-impression-3d"),
    path('decoupe-laser/' , decoupe_laser, name="services-laser"),
    path('fraiseuse-numerique/' , fraiseuse_numerique, name="services-fraiseuse"),
    path('broderie-numerique/' , broderie_numerique, name="services-broderie"),
    path('impression-numerique-propose', impression_num_proposees, name="service-impression-numerique-propose"),
    path('broderie-order', save_broderie_order, name='broderie-order'),
]
