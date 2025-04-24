from django.urls import path

from Formations.views import broder_num, Decoupe_laser, Fraiseuse_num , impression_3d, impression_num

app_name = "activities"

urlpatterns = [
    path('broder_num/', broder_num, name='broder_num'),
    path('Decoupe_laser/', Decoupe_laser, name='Decoupe_laser'),
    path('Fraiseuse_num/', Fraiseuse_num, name='Fraiseuse_num'),
    path('impression_3d/', impression_3d, name='impression_3d'),
    path('impression_num/', impression_num, name='impression_num'),
]