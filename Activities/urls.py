from django.urls import path

from .views import smart_coders, fab_elle, fab_tour

urlpatterns = [
    path('smart_coders/', smart_coders, name='smart_coders'),
    path('fab_elle/', fab_elle, name='fab_elle'),
    path('fab_tour/', fab_tour, name='fab_tour'),
]