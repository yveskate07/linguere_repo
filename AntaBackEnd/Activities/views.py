from django.shortcuts import render

# Create your views here.
def smart_coders(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for smart_coders requested
    """
    return render(request, "Activities/smart_coders/index.html")

def fab_elle(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for fab_elle requested
    """
    return render(request, "Activities/fab_elle/index.html")

def fab_tour(request):
    """
    :param request: contains all the infos of the request, ex user's data, browser's data etc
    :return: the template for fab_tour requested
    """
    return render(request, "Activities/fab_tour/index.html")