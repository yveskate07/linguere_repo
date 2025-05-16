from django.shortcuts import render

from Services.forms import Broderie_num_customForm, Fraiseuse_customForm, Laser_customForm, Imp_3D_customForm, \
    Imp_Num_customForm
from Services.models import ClientCustomizationForBroderieNumerique, Service


# Create your views here.
def broderie_numerique(request):
    service = Service.objects.get(name="Broderie Numérique")
    return render(request, "Services/broderie/index.html", {'broderie_form':Broderie_num_customForm(),
                                                            'brod_serviceName':service.name,
                                                            'brod_serviceDesc': service.description,
                                                            'img1':service.image1.url,'img2':service.image2.url,'img3':service.image3.url,'img4':service.image4.url,
                                                            'img5':service.image5.url,'img6':service.image6.url,'img7':service.image7.url,'img8':service.image8.url})

def fraiseuse_numerique(request):
    service = Service.objects.get(name="Service de Fraiseuse Numérique (CNC)")
    return render(request, "Services/fraiseuse/index.html", {'fraiseuse_form':Fraiseuse_customForm(),
                                                             'frais_serviceName': service.name,
                                                             'frais_serviceDesc': service.description,
                                                            'img1':service.image1.url,'img2':service.image2.url,'img3':service.image3.url,'img4':service.image4.url,
                                                            'img5':service.image5.url,'img6':service.image6.url,'img7':service.image7.url,'img8':service.image8.url})

def decoupe_laser(request):
    service = Service.objects.get(name="Découpe et Gravure Laser")
    return render(request, "Services/laser/index.html",{'laser_form':Laser_customForm(),
                                                            'laser_serviceName': service.name,
                                                            'laser_serviceDesc': service.description,
                                                            'img1':service.image1.url,'img2':service.image2.url,'img3':service.image3.url,'img4':service.image4.url,
                                                            'img5':service.image5.url,'img6':service.image6.url,'img7':service.image7.url,'img8':service.image8.url})

def impression_3D(request):
    service = Service.objects.get(name="Service d’Impression 3D")
    return render(request, 'Services/Impre_3D/index.html',{'imp_3D_form':Imp_3D_customForm(),
                                                            'imp_3D_serviceName': service.name,
                                                            'imp_3D_serviceDesc': service.description,
                                                            'img1':service.image1.url,'img2':service.image2.url,'img3':service.image3.url,'img4':service.image4.url,
                                                            'img5':service.image5.url,'img6':service.image6.url,'img7':service.image7.url,'img8':service.image8.url})

def impression_num_proposees(request):
    service = Service.objects.get(name="Types d’Impressions Numériques Proposées")
    return render(request, 'Services/Impre_Num/index.html',{'imp_num_form':Imp_Num_customForm(),
                                                            'imp_num_serviceName': service.name,
                                                            'imp_num_serviceDesc': service.description,
                                                            'img1':service.image1.url,'img2':service.image2.url,'img3':service.image3.url,'img4':service.image4.url,
                                                            'img5':service.image5.url,'img6':service.image6.url,'img7':service.image7.url,'img8':service.image8.url})


def save_client_data(function):
    def pre_save(*args, **kwargs):

        if args:
            request = args[0]
            if request.method == "POST":
                kwargs['name'] = request.POST.get("name")
                kwargs['email'] = request.POST.get("email")
                kwargs['tel_number'] = request.POST.get("tel_number")
                kwargs['town'] = request.POST.get("town")
                kwargs['delivery_mode'] = request.POST.get("delivery_mode")
                kwargs['cgu_accept'] = request.POST.get("cgu_accept")

                return function(*args, **kwargs)

    return pre_save


def save_broderie_order(request):

    if request.method == "POST":
        print(request.POST)
    """support_type = request['support_type']
    dim_1 = request['dim_1']
    dim_2 = request['dim_2']
    quantity = request['quantity']
    special_instructions = request['special_instructions']

    order = ClientCustomizationForBroderieNumerique.objects.create(support_type=support_type,
                                                                   dim_1=dim_1,
                                                                   dim_2=dim_2,
                                                                   quantity=quantity,
                                                                   special_instructions=special_instructions,
                                                                   name = kwargs['name'],
                                                                   email = kwargs['email'],
                                                                   tel_number = kwargs['tel_number'],
                                                                   town = kwargs['town'],
                                                                   delivery_mode = kwargs['delivery_mode'],
                                                                   cgu_accept = kwargs['cgu_accept']
                                                                   )
    order.save()"""

def save_fraiseuse_order(request):
    if request.method == "POST":
        print(request.POST)

def save_laser_order(request):
    if request.method == "POST":
        print(request.POST)

def save_imp_num_order(request):
    if request.method == "POST":
        print(request.POST)

def save_imp_3d_order(request):
    if request.method == "POST":
        print(request.POST)