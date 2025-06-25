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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from AntaBackEnd import views, settings

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('location/', views.location, name='location'),
    path('about', views.about, name="about"),
    path('shop/', include("Shop.urls")),
    path('services/', include("Services.urls")),
    path('activities/', include("Activities.urls")),
    path('formations/',include('Formations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)