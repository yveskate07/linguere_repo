from django.shortcuts import render

# Create your views here.
def broderie(request):
    return render(request, "Services/broderie/index.html")

def CNC(request):
    return render(request, "Services/CNC/index.html")

def laser(request):
    return render(request, "Services/laser/index.html")