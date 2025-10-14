import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .models import Activity


# Create your views here.

def get_context_for_activities(request, activity_name):
    user_id = request.user.id if request.user.is_authenticated else 'anonymous_id'
    try:
        activity = Activity.objects.get(name=activity_name)
    except Exception as e:
        return HttpResponse("Cette activité n'existe pas !")
    else:
        return {
            'activity': activity,
            'realisations': activity.realisations.all(),
            'resultats': activity.resultats.all(),
            'impacts': activity.impacts.all(),
            'galerie_images': activity.galerie_images.all(),
            'user_id': user_id,
        }


def smart_coders(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for smart_coders requested
    """

    context = get_context_for_activities(request, "Smart Coders")

    return render(request, "Activities/index.html", context=context)


def fab_elle(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for fab_elle requested
    """

    context = get_context_for_activities(request, "Fab'Elles")
    
    return render(request, "Activities/index.html", context=context)


def fab_tour(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for fab_tour requested
    """

    context = get_context_for_activities(request, "Fab'Tour")
    
    return render(request, "Activities/index.html", context=context)