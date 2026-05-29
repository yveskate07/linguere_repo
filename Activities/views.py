import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .models import Activity


# Create your views here.

def activityView(request, slug):
    try:
        activity = Activity.objects.get(slug=slug)
    except Exception as e:
        return HttpResponse("Cette activité n'existe pas !")
    else:
        context = {
            'activity': activity,
            'realisations': activity.realisations.all(),
            'resultats': activity.resultats.all()[0],
            'impacts': activity.impacts.all(),
            'galerie_images': activity.galerie_images.all(),
        }

        return render(request, "Activities/index.html", context=context)