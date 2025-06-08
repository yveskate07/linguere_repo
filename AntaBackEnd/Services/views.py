import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from Services.forms import Broderie_num_customForm1, Fraiseuse_customForm1, Laser_customForm1, Imp_3D_customForm1, \
    Broderie_num_customForm2, Fraiseuse_customForm2, Laser_customForm2, Imp_3D_customForm2, Paper_customForm1, \
    Paper_customForm2, Textile_customForm1, Textile_customForm2, Objects_customForm1, Objects_customForm2
from Services.models import Service


# Create your views here.
def broderie_numerique(request):
    service = Service.objects.get(name="Broderie Numérique")
    return render(request, "Services/broderie/index.html", {'broderie_form1': Broderie_num_customForm1(),
                                                            'broderie_form2': Broderie_num_customForm2(),
                                                            'service_id': service.pk,
                                                            'brod_serviceName': service.name,
                                                            'brod_serviceDesc': service.description,
                                                            'img1': service.image1.url, 'img2': service.image2.url,
                                                            'img3': service.image3.url, 'img4': service.image4.url,
                                                            'img5': service.image5.url, 'img6': service.image6.url,
                                                            'img7': service.image7.url, 'img8': service.image8.url})


def fraiseuse_numerique(request):
    service = Service.objects.get(name="Service de Fraiseuse Numérique (CNC)")
    return render(request, "Services/fraiseuse/index.html", {'fraiseuse_form1': Fraiseuse_customForm1(),
                                                             'fraiseuse_form2': Fraiseuse_customForm2(),
                                                             'service_id': service.pk,
                                                             'frais_serviceName': service.name,
                                                             'frais_serviceDesc': service.description,
                                                             'img1': service.image1.url, 'img2': service.image2.url,
                                                             'img3': service.image3.url, 'img4': service.image4.url,
                                                             'img5': service.image5.url, 'img6': service.image6.url,
                                                             'img7': service.image7.url, 'img8': service.image8.url})


def decoupe_laser(request):
    service = Service.objects.get(name="Découpe et Gravure Laser")
    return render(request, "Services/laser/index.html", {'laser_form1': Laser_customForm1(),
                                                         'laser_form2': Laser_customForm2(),
                                                         'service_id': service.pk,
                                                         'laser_serviceName': service.name,
                                                         'laser_serviceDesc': service.description,
                                                         'img1': service.image1.url, 'img2': service.image2.url,
                                                         'img3': service.image3.url, 'img4': service.image4.url,
                                                         'img5': service.image5.url, 'img6': service.image6.url,
                                                         'img7': service.image7.url, 'img8': service.image8.url})


def impression_3D(request):
    service = Service.objects.get(name="Service d’Impression 3D")
    return render(request, 'Services/Impre_3D/index.html', {'imp_3D_form1': Imp_3D_customForm1(),
                                                            'imp_3D_form2': Imp_3D_customForm2(),
                                                            'service_id': service.pk,
                                                            'imp_3D_serviceName': service.name,
                                                            'imp_3D_serviceDesc': service.description,
                                                            'img1': service.image1.url, 'img2': service.image2.url,
                                                            'img3': service.image3.url, 'img4': service.image4.url,
                                                            'img5': service.image5.url, 'img6': service.image6.url,
                                                            'img7': service.image7.url, 'img8': service.image8.url})


def impression_num_papiers(request):
    service = Service.objects.get(name="Impression sur Papier et Supports Rigides")
    return render(request, 'Services/Impre_Num_Prop/paper_solid_support/index.html',
                  {'paper_form1': Paper_customForm1(),
                   'paper_form2': Paper_customForm2(),
                   'paper_serviceName': service.name,
                   'paper_serviceDesc': service.description,
                   'service_id': service.pk,
                   'img1': service.image1.url, 'img2': service.image2.url, 'img3': service.image3.url,
                   'img4': service.image4.url,
                   'img5': service.image5.url, 'img6': service.image6.url, 'img7': service.image7.url,
                   'img8': service.image8.url})


def impression_num_textile(request):
    service = Service.objects.get(name="Impression sur Textiles et Vêtements")
    return render(request, 'Services/Impre_Num_Prop/textile_vetements/index.html',
                  {'textile_form1': Textile_customForm1(),
                   'textile_form2': Textile_customForm2(),
                   'textile_serviceName': service.name,
                   'textile_serviceDesc': service.description,
                   'service_id': service.pk,
                   'img1': service.image1.url, 'img2': service.image2.url, 'img3': service.image3.url,
                   'img4': service.image4.url,
                   'img5': service.image5.url, 'img6': service.image6.url, 'img7': service.image7.url,
                   'img8': service.image8.url})


def impression_num_objects(request):
    service = Service.objects.get(name="Impression sur Objets Personnalisés")
    return render(request, 'Services/Impre_Num_Prop/others_objects/index.html', {'object_form1': Objects_customForm1(),
                                                                                 'object_form2': Objects_customForm2(),
                                                                                 'object_serviceName': service.name,
                                                                                 'object_serviceDesc': service.description,
                                                                                 'service_id': service.pk,
                                                                                 'img1': service.image1.url,
                                                                                 'img2': service.image2.url,
                                                                                 'img3': service.image3.url,
                                                                                 'img4': service.image4.url,
                                                                                 'img5': service.image5.url,
                                                                                 'img6': service.image6.url,
                                                                                 'img7': service.image7.url,
                                                                                 'img8': service.image8.url})


def save_broderie_order(request):
    if request.method == 'POST':
        if request.POST.get("with-upload-design") == '0':
            form = Broderie_num_customForm1({'support_type': request.POST.get('support_type'),
                                             'other_support': request.POST.get('other_support'),
                                             'dim_1': request.POST.get('dim_1'),
                                             'dim_2': request.POST.get('dim_2'),
                                             'quantity': request.POST.get('quantity'),
                                             'special_instructions': request.POST.get('special_instructions'),
                                             'design_picture': request.POST.get('design_picture'),
                                             'codeCouleur': request.POST.get('codeCouleur'),
                                             'name': request.POST.get('name'),
                                             'email': request.POST.get('email'),
                                             'tel_number': request.POST.get('tel_number'),
                                             'town': request.POST.get('town'),
                                             'delivery_mode': request.POST.get('delivery_mode'),
                                             'cgu_accept': request.POST.get('cgu_accept')})

        else:
            form = form = Broderie_num_customForm2({'support_type': request.POST.get('support_type'),
                                                    'other_support': request.POST.get('other_support'),
                                                    'dim_1': request.POST.get('dim_1'),
                                                    'dim_2': request.POST.get('dim_2'),
                                                    'quantity': request.POST.get('quantity'),
                                                    'special_instructions': request.POST.get('special_instructions'),
                                                    'upload_design_picture': request.POST.get('upload_design_picture'),
                                                    'codeCouleur': request.POST.get('codeCouleur'),
                                                    'name': request.POST.get('name'),
                                                    'email': request.POST.get('email'),
                                                    'tel_number': request.POST.get('tel_number'),
                                                    'town': request.POST.get('town'),
                                                    'delivery_mode': request.POST.get('delivery_mode'),
                                                    'cgu_accept': request.POST.get('cgu_accept')}, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()
            # envoi d'un email
            return HttpResponse("Felicitations votre commande a été enregistrée ")

        else:
            return HttpResponse(f"Erreur : {form.errors}")


def save_fraiseuse_order(request):
    if request.method == 'POST':
        if request.POST.get("with-upload-design") == '0':
            form = Fraiseuse_customForm1({'service_type': request.POST.get('service_type'),
                                          'dim_1': request.POST.get('dim_1'),
                                          'dim_2': request.POST.get('dim_2'),
                                          'quantity': request.POST.get('quantity'),
                                          'special_instructions': request.POST.get('special_instructions'),
                                          'design_picture': request.POST.get('design_picture'),
                                          'used_materials': request.POST.get('used_materials'),
                                          'name': request.POST.get('name'),
                                          'email': request.POST.get('email'),
                                          'tel_number': request.POST.get('tel_number'),
                                          'town': request.POST.get('town'),
                                          'delivery_mode': request.POST.get('delivery_mode'),
                                          'cgu_accept': request.POST.get('cgu_accept')})

        else:
            form = form = Fraiseuse_customForm2({'service_type': request.POST.get('service_type'),
                                                 'dim_1': request.POST.get('dim_1'),
                                                 'dim_2': request.POST.get('dim_2'),
                                                 'quantity': request.POST.get('quantity'),
                                                 'special_instructions': request.POST.get('special_instructions'),
                                                 'upload_design_picture': request.POST.get('upload_design_picture'),
                                                 'used_materials': request.POST.get('used_materials'),
                                                 'name': request.POST.get('name'),
                                                 'email': request.POST.get('email'),
                                                 'tel_number': request.POST.get('tel_number'),
                                                 'town': request.POST.get('town'),
                                                 'delivery_mode': request.POST.get('delivery_mode'),
                                                 'cgu_accept': request.POST.get('cgu_accept')}, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()
            # envoi d'un email
            return HttpResponse("Felicitations votre commande a été enregistrée ")

        else:
            return HttpResponse(f"Erreur : {form.errors}")

def save_laser_order(request):
    if request.method == 'POST':
        if request.POST.get("with-upload-design") == '0':
            form = Laser_customForm1({'service_type': request.POST.get('service_type'),
                                      'dim_1': request.POST.get('dim_1'),
                                      'dim_2': request.POST.get('dim_2'),
                                      'quantity': request.POST.get('quantity'),
                                      'special_instructions': request.POST.get('special_instructions'),
                                      'design_picture': request.POST.get('design_picture'),
                                      'used_materials': request.POST.get('used_materials'),
                                      'name': request.POST.get('name'),
                                      'email': request.POST.get('email'),
                                      'tel_number': request.POST.get('tel_number'),
                                      'town': request.POST.get('town'),
                                      'delivery_mode': request.POST.get('delivery_mode'),
                                      'cgu_accept': request.POST.get('cgu_accept')})

        else:
            form = form = Laser_customForm2({'service_type': request.POST.get('service_type'),
                                             'dim_1': request.POST.get('dim_1'),
                                             'dim_2': request.POST.get('dim_2'),
                                             'quantity': request.POST.get('quantity'),
                                             'special_instructions': request.POST.get('special_instructions'),
                                             'upload_design_picture': request.POST.get('upload_design_picture'),
                                             'used_materials': request.POST.get('used_materials'),
                                             'name': request.POST.get('name'),
                                             'email': request.POST.get('email'),
                                             'tel_number': request.POST.get('tel_number'),
                                             'town': request.POST.get('town'),
                                             'delivery_mode': request.POST.get('delivery_mode'),
                                             'cgu_accept': request.POST.get('cgu_accept')}, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()
            # envoi d'un email
            return HttpResponse("Felicitations votre commande a été enregistrée ")

        else:
            return HttpResponse(f"Erreur : {form.errors}")

def save_imp_3d_order(request):
    if request.method == 'POST':
        if request.POST.get("with-upload-design") == '0':
            form = Imp_3D_customForm1({'impression_type': request.POST.get('impression_type'),
                                       'dim_1': request.POST.get('dim_1'),
                                       'dim_2': request.POST.get('dim_2'),
                                       'quantity': request.POST.get('quantity'),
                                       'codeCouleur': request.POST.get('codeCouleur'),
                                       'special_instructions': request.POST.get('special_instructions'),
                                       'design_picture': request.POST.get('design_picture'),
                                       'used_materials': request.POST.get('used_materials'),
                                       'name': request.POST.get('name'),
                                       'email': request.POST.get('email'),
                                       'tel_number': request.POST.get('tel_number'),
                                       'town': request.POST.get('town'),
                                       'delivery_mode': request.POST.get('delivery_mode'),
                                       'cgu_accept': request.POST.get('cgu_accept')})

        else:
            form = Imp_3D_customForm2({'impression_type': request.POST.get('impression_type'),
                                              'dim_1': request.POST.get('dim_1'),
                                              'dim_2': request.POST.get('dim_2'),
                                              'quantity': request.POST.get('quantity'),
                                              'codeCouleur': request.POST.get('codeCouleur'),
                                              'special_instructions': request.POST.get('special_instructions'),
                                              'upload_design_picture': request.POST.get('upload_design_picture'),
                                              'used_materials': request.POST.get('used_materials'),
                                              'name': request.POST.get('name'),
                                              'email': request.POST.get('email'),
                                              'tel_number': request.POST.get('tel_number'),
                                              'town': request.POST.get('town'),
                                              'delivery_mode': request.POST.get('delivery_mode'),
                                              'cgu_accept': request.POST.get('cgu_accept')}, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()
            # envoi d'un email
            return HttpResponse("Felicitations votre commande a été enregistrée ")

        else:
            return HttpResponse(f"Erreur : {form.errors}")

def save_imp_text_order(request):
    if request.method == "POST":
        if request.POST.get("with-upload-design") == '0':
            form_data = {field: request.POST.get(field) for field in Textile_customForm1.Meta.fields}
            form = Textile_customForm1(form_data)

        else:
            form_data = {field: request.POST.get(field) for field in Textile_customForm2.Meta.fields}
            form_data['upload_design_picture'] = request.FILES.get('upload_design_picture')
            form = Textile_customForm2(form_data)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()
            # envoi d'un email
            return HttpResponse("Felicitations votre commande a été enregistrée ")

        else:
            return HttpResponse(f"Erreur : {form.errors}")

def save_imp_paper_order(request):
    if request.method == "POST":
        if request.POST.get("with-upload-design") == '0':
            form_data = {field: request.POST.get(field) for field in Paper_customForm1.Meta.fields}
            form = Paper_customForm1(form_data)

        else:
            form_data = {field: request.POST.get(field) for field in Paper_customForm2.Meta.fields}
            form_data['upload_design_picture'] = request.FILES.get('upload_design_picture')
            form = Paper_customForm2(form_data)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()
            # envoi d'un email
            return HttpResponse("Felicitations votre commande a été enregistrée ")
        else:
            return HttpResponse(f"Erreur : {form.errors}")
    
def save_imp_object_order(request):
    if request.method == "POST":
        if request.POST.get("with-upload-design") == '0':
            form_data = {field: request.POST.get(field) for field in Objects_customForm1.Meta.fields}
            form = Objects_customForm1(form_data)

        else:
            form_data = {field: request.POST.get(field) for field in Objects_customForm2.Meta.fields}
            form_data['upload_design_picture'] = request.FILES.get('upload_design_picture')
            form = Objects_customForm2(form_data)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = Service.objects.get(pk=int(request.POST.get("service")))
            order.save()
            # envoi d'un email
            return HttpResponse("Felicitations votre commande a été enregistrée ")
        else:
            return HttpResponse(f"Erreur : {form.errors}")