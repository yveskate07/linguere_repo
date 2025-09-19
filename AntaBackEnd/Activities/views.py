import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Activities.models import Activity


# Create your views here.

def get_context_for_activities(request, activity_name):
    user_id = request.user
    activity = Activity.objects.get(name=activity_name)
    return {
        'activity': activity,
        'realisations': activity.realisations.all(),
        'resultats': activity.resultats.all(),
        'impacts': activity.impacts.all(),
        'galerie_images': activity.galerie_images.all()
    }

@login_required
def smart_coders(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for smart_coders requested
    """

    context = get_context_for_activities(request, "Smart Coders")
    user_id = request.user
    context['user_id'] = user_id

    return render(request, "Activities/index.html", context=context)

@login_required
def fab_elle(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for fab_elle requested
    """

    user_id = request.user
    context = get_context_for_activities(request, "Fab'Elles")
    context['user_id'] = user_id
    return render(request, "Activities/index.html", context=context)

@login_required
def fab_tour(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for fab_tour requested
    """

    user_id = request.user
    context = get_context_for_activities(request, "Fab'Tour")
    context['user_id'] = user_id
    return render(request, "Activities/index.html", context=context)