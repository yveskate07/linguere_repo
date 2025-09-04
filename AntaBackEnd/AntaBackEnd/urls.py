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
from django.contrib.auth import views as auth_views

from AntaBackEnd.views import cart_view

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('logout/', views.FabLabLogoutView.as_view(), name='logout'),
    path('location/', views.location, name='location'),
    path('about/', views.about, name="about"),
    path('sign-up/', views.SignUpView.as_view(), name="sign-up"),
    path('login/', views.FabLabLoginView.as_view(), name='login'),
    path('shop/', include("Shop.urls")),
    path('services/', include("Services.urls")),
    path('activities/', include("Activities.urls")),
    path('formations/',include('Formations.urls')),
    path('user/', include('Users.urls')),
    path('cart/', cart_view, name='cart'),
    path('password-reset/', views.FabPassResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.FabPasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)