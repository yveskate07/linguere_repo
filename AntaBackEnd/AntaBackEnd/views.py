from django.shortcuts import HttpResponseRedirect, render


def home(request):
    return render(request,'AntaBackEnd/accueil/index.html')

def location(request):
    return render(request, 'AntaBackEnd/location/index.html')

def about(request):
    return render(request, "AntaBackEnd/about/index.html")