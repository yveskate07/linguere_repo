from django.urls import path
from . import views

urlpatterns = [
    # Une seule URL pour tous les services — le slug identifie le service
    path('<slug:slug>/', views.service_view, name='service'),
]