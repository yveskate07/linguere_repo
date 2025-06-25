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
from .views import broderie_numerique, fraiseuse_numerique, decoupe_laser, impression_3D, \
    save_broderie_order, save_fraiseuse_order, save_laser_order, save_imp_3d_order, \
    impression_num_papiers, impression_num_textile, impression_num_objects, save_imp_paper_order, save_imp_text_order, \
    save_imp_object_order

urlpatterns = [
    path('impression-3d/' , impression_3D, name="service-impression-3d"),
    path('decoupe-laser/' , decoupe_laser, name="services-laser"),
    path('fraiseuse-numerique/' , fraiseuse_numerique, name="services-fraiseuse"),
    path('broderie-numerique/' , broderie_numerique, name="services-broderie"),
    path('impression-numerique-papiers/', impression_num_papiers, name="service-impression-numerique-papiers"),
    path('impression-numerique-textile/', impression_num_textile, name="service-impression-numerique-textile"),
    path('impression-numerique-objets/', impression_num_objects, name="service-impression-numerique-objets"),
    path('broderie-order', save_broderie_order, name='broderie-order'),
    path('fraiseuse-order', save_fraiseuse_order, name='fraiseuse-order'),
    path('laser-order', save_laser_order, name='laser-order'),
    path('imp-paper-order', save_imp_paper_order, name='imp-paper-order'),
    path('imp-text-order', save_imp_text_order, name='imp-text-order'),
    path('imp-object-order', save_imp_object_order, name='imp-object-order'),
    path('imp-3d-order', save_imp_3d_order, name='imp-3d-order'),
]
