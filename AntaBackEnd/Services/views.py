from django.shortcuts import render

# Create your views here.
def broderie_numerique(request): 
    return render(request, "Services/broderie/index.html")

def fraiseuse_numerique(request):
    return render(request, "Services/CNC/index.html")

def decoupe_laser(request):
    return render(request, "Services/laser/index.html")

def impression_3D(request):
    return render(request, 'Services/Impre_3D/index.html')

def impression_num_proposees(request):
    return render(request, 'Services/Impre_Num/index.html')