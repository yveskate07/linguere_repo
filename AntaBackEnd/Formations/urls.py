from django.urls import path

from Formations.views import returnBrochure, SigningUp, userGetInTouch, formationView

app_name = "formations"

urlpatterns = [
    path('<str:formation_name>/',formationView, name="formationView"),
    path('get-brochure/<str:formation_name>/', returnBrochure, name='get-brochure'),
    path('sign-up/<str:formation_name>/',SigningUp, name="signup"),
    path('get-in-touch/<str:formation_name>/', userGetInTouch, name="get-in-touch")
]