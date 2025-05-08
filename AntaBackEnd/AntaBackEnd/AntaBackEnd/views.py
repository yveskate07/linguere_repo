from django.shortcuts import HttpResponseRedirect, render
from Formations.models import Formations

def home(request):

    broderie_num = Formations.objects.get(name="Broderie Numérique")
    fraiseuse_num = Formations.objects.get(name="Fraiseuse Numérique (CNC)")
    impression_3d = Formations.objects.get(name="Impression 3D")
    impression_num = Formations.objects.get(name="Impression Numérique")
    laser = Formations.objects.get(name="Découpe Laser")

    return render(request,'AntaBackEnd/accueil/index.html',
                  {'broderie_num_slug': broderie_num.slug,
                        'fraiseuse_num_slug': fraiseuse_num.slug,
                        'impression_3d_slug': impression_3d.slug,
                        'impression_num_slug': impression_num.slug,
                        'laser_slug': laser.slug}
                  )

def location(request):
    return render(request, 'AntaBackEnd/location/index.html')

def about(request):
    return render(request, "AntaBackEnd/about/index.html")