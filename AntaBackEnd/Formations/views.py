from django.shortcuts import render

# Create your views here.
def broderie_num(request):
    return render(request, "Formations/broderie_num/index.html")

def laser(request):
    return render(request, "Formations/laser/index.html")

def fraiseuse_num(request):
    return render(request, "Formations/fraiseuse_num/index.html")

def impression_3d(request):
    return render(request, "Formations/impression_3d/index.html")

def impression_num(request):
    return render(request, "Formations/impression_num/index.html")