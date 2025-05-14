from django.shortcuts import render

from Services.forms import Broderie_num_customForm
from Services.models import ClientCustomizationForBroderieNumerique, Service


# Create your views here.
def broderie_numerique(request):
    service = Service.objects.get(name="Broderie Numérique")
    return render(request, "Services/broderie/index.html", {'broderie_form':Broderie_num_customForm(),
                                                            'brod_serviceName':service.name,
                                                            'brod_serviceDesc': service.description,
                                                            'img1':service.image1.url or '','img2':service.image2.url or '','img3':service.image3.url or '','img4':service.image4.url or '',
                                                            'img5':service.image5.url or '','img6':service.image6.url or '','img7':service.image7.url or '','img8':service.image8.url or ''})

def fraiseuse_numerique(request):
    service = Service.objects.get(name="Service de Fraiseuse Numérique (CNC)", )
    return render(request, "Services/fraiseuse/index.html")

def decoupe_laser(request):
    return render(request, "Services/laser/index.html")

def impression_3D(request):
    return render(request, 'Services/Impre_3D/index.html')

def impression_num_proposees(request):
    return render(request, 'Services/Impre_Num/index.html')


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

