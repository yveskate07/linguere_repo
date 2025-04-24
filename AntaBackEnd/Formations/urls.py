from django.urls import path

from Formations.views import broderie_num, laser, fraiseuse_num , impression_3d, impression_num

app_name = "formations"

urlpatterns = [
    path('broderie_num/', broderie_num, name='broderie_num'),
    path('laser/', laser, name='laser'),
    path('fraiseuse_num/', fraiseuse_num, name='fraiseuse_num'),
    path('impression_3d/', impression_3d, name='impression_3d'),
    path('impression_num/', impression_num, name='impression_num'),
]