import json

from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Services.forms import Broderie_num_customForm1, Fraiseuse_customForm1, Laser_customForm1, Imp_3D_customForm1, \
    Broderie_num_customForm2, Fraiseuse_customForm2, Laser_customForm2, Imp_3D_customForm2, Paper_customForm1, \
    Paper_customForm2, Textile_customForm1, Textile_customForm2, Objects_customForm1, Objects_customForm2
from Services.models import Service
from Shop.services.cart_service import CartService
from mail_sender import mail_to_the_client, mail_to_fablab


def get_msg_for_client_mail(Service_name, obj, width, height, quantite, comment, msg_deliver, img_path=None, colors=None, request=None):

    if colors:
        colors = [i.lstrip('#') for i in colors]

    msg_body = render_to_string(request=request, template_name="Services/mail_for_users/index.html", context={'Service_name':Service_name,
                                                                                                              'obj':obj,
                                                                                                              'width':width,
                                                                                                              'height':height,
                                                                                                              'quantite':quantite,
                                                                                                              'comment':comment,
                                                                                                              'img_path':img_path,
                                                                                                              'msg_deliver':msg_deliver,
                                                                                                              'colors_list':colors
                                                                                                              }
                                                                                                             )
    with open("code1.html",'w') as f:
        f.write(msg_body)

    return msg_body

def get_msg_for_admin_mail(request , **kwargs):
    admin_url = reverse('admin:index')
    absolute_admin_url = request.build_absolute_uri(admin_url)
    colors = kwargs.get('colors', None)

    if colors:
        colors = [i.lstrip('#') for i in kwargs['colors']]

    msg_body = render_to_string(request=request, template_name="Services/mail_for_fablab/index.html",
                                context={'colors_list':colors,
                                         'Service_name': kwargs['service'],
                                         'obj': kwargs['obj'],
                                         'width': kwargs['width'],
                                         'height': kwargs['height'],
                                         'quantite': kwargs['quantity'],
                                         'comment': kwargs['comment'],
                                         'img_path': kwargs['img_path'],
                                         'deliver': kwargs['delivery'],
                                         'name':kwargs.get('name'),
                                         'email':kwargs.get('email'),
                                         'tel_number':kwargs.get('tel_number'),
                                         'town':kwargs.get('town'),
                                         'absolute_admin_url':absolute_admin_url
                                         }
                                )
    with open("code2.html",'w') as f:
        f.write(msg_body)

    return msg_body

# Create your views here.
@login_required
def broderie_numerique(request, errors_txt=None, errors=0):
    service = Service.objects.get(name="Broderie Numérique")
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Services/broderie/index.html", {'broderie_form1': Broderie_num_customForm1(),
                                                            'broderie_form2': Broderie_num_customForm2(),
                                                            'service_id': service.pk,
                                                            'brod_serviceName': service.name,
                                                            'brod_serviceDesc': service.description,
                                                            
                                                            'user_id': request.user.id,
                                                            'img_urls': [image.url for image in service.galerie_images.all()] if service.galerie_images.all() else None,
                                                            'img1': service.image1.url, 'img2': service.image2.url,
                                                            'img3': service.image3.url, 'img4': service.image4.url,
                                                            'img5': service.image5.url, 'img6': service.image6.url,
                                                            'img7': service.image7.url, 'img8': service.image8.url,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
                                                            'errors': errors,'errors_txt':errors_txt})

@login_required
def fraiseuse_numerique(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Service de Fraiseuse Numérique (CNC)")
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Services/fraiseuse/index.html", {'fraiseuse_form1': Fraiseuse_customForm1(),
                                                             'fraiseuse_form2': Fraiseuse_customForm2(),
                                                             'service_id': service.pk,
                                                             'frais_serviceName': service.name,
                                                             'frais_serviceDesc': service.description,
                                                             
                                                             'user_id': request.user.id,
                                                             'img1': service.image1.url, 'img2': service.image2.url,
                                                             'img3': service.image3.url, 'img4': service.image4.url,
                                                             'img5': service.image5.url, 'img6': service.image6.url,
                                                             'img7': service.image7.url, 'img8': service.image8.url,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
                                                             'errors': errors,'errors_txt':errors_txt})

@login_required
def decoupe_laser(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Découpe et Gravure Laser")
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, "Services/laser/index.html", {'laser_form1': Laser_customForm1(),
                                                         'laser_form2': Laser_customForm2(),
                                                         'service_id': service.pk,
                                                         'laser_serviceName': service.name,
                                                         'laser_serviceDesc': service.description,
                                                         
                                                         'user_id': request.user.id,
                                                         'img1': service.image1.url, 'img2': service.image2.url,
                                                         'img3': service.image3.url, 'img4': service.image4.url,
                                                         'img5': service.image5.url, 'img6': service.image6.url,
                                                         'img7': service.image7.url, 'img8': service.image8.url,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
                                                         'errors': errors,'errors_txt':errors_txt})

@login_required
def impression_3D(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Service d'Impression 3D")
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, 'Services/Impre_3D/index.html', {'imp_3D_form1': Imp_3D_customForm1(),
                                                            'imp_3D_form2': Imp_3D_customForm2(),
                                                            'service_id': service.pk,
                                                            'imp_3D_serviceName': service.name,
                                                            'imp_3D_serviceDesc': service.description,
                                                            
                                                            'user_id': request.user.id,
                                                            'img1': service.image1.url, 'img2': service.image2.url,
                                                            'img3': service.image3.url, 'img4': service.image4.url,
                                                            'img5': service.image5.url, 'img6': service.image6.url,
                                                            'img7': service.image7.url, 'img8': service.image8.url,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
                                                            'errors': errors,'errors_txt':errors_txt})

@login_required
def impression_num_papiers(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Impression sur Papier et Supports Rigides")
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, 'Services/Impre_Num_Prop/paper_solid_support/index.html',
                  {'paper_form1': Paper_customForm1(),
                   'paper_form2': Paper_customForm2(),
                   'paper_serviceName': service.name,
                   'paper_serviceDesc': service.description,
                   
                   'user_id': request.user.id,
                   'service_id': service.pk,
                   'img1': service.image1.url, 'img2': service.image2.url, 'img3': service.image3.url,
                   'img4': service.image4.url,
                   'img5': service.image5.url, 'img6': service.image6.url, 'img7': service.image7.url,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
                   'img8': service.image8.url, 'errors': errors,'errors_txt':errors_txt})

@login_required
def impression_num_textile(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Impression sur Textiles et Vêtements")
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, 'Services/Impre_Num_Prop/textile_vetements/index.html',
                  {'textile_form1': Textile_customForm1(),
                   'textile_form2': Textile_customForm2(),
                   'textile_serviceName': service.name,
                   'textile_serviceDesc': service.description,
                   
                   'user_id': request.user.id,
                   'service_id': service.pk,
                   'img1': service.image1.url, 'img2': service.image2.url, 'img3': service.image3.url,
                   'img4': service.image4.url,
                   'img5': service.image5.url, 'img6': service.image6.url, 'img7': service.image7.url,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
                   'img8': service.image8.url, 'errors': errors,'errors_txt':errors_txt})

@login_required
def impression_num_objects(request, errors_txt=None, errors=0, success=0, success_txt=None):
    service = Service.objects.get(name="Impression sur Objets Personnalisés")
    products_cart = CartService.get_cart_data_from_request(request)
    return render(request, 'Services/Impre_Num_Prop/others_objects/index.html', {'object_form1': Objects_customForm1(),
                                                                                 'object_form2': Objects_customForm2(),
                                                                                 'object_serviceName': service.name,
                                                                                 'object_serviceDesc': service.description,
                                                                                 
                                                                                 'user_id': request.user.id,
                                                                                 'service_id': service.pk,
                                                                                 'img1': service.image1.url,
                                                                                 'img2': service.image2.url,
                                                                                 'img3': service.image3.url,
                                                                                 'img4': service.image4.url,
                                                                                 'img5': service.image5.url,
                                                                                 'img6': service.image6.url,
                                                                                 'img7': service.image7.url,
                                                                                 'img8': service.image8.url,
        'products_cart': products_cart['products'],
        'products_cart_js': json.dumps(products_cart['products']),
        'total_price_cart': products_cart['total_price'],
                                                                                 'errors': errors,'errors_txt':errors_txt})

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

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)
            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""


            msg_body1 = get_msg_for_client_mail(request = request, Service_name='Broderie',
                                                obj=request.POST.get('support_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                colors=request.POST.get('codeCouleur').split(','),
                                                comment = request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service="Broderie Numérique", obj=request.POST.get('support_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               img_path=design_path,
                                               colors=request.POST.get('codeCouleur').split(','),
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Broderie Numérique")

            return broderie_numerique(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return broderie_numerique(request, errors=1, errors_txt=errors)

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

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(request = request, Service_name='Fraiseuse',
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                img_path=design_path,
                                                quantite=request.POST.get('quantity'),
                                                comment=request.POST.get('special_instructions'),
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service="Fraiseuse Numérique", obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               img_path=design_path,
                                               colors=None,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body1,
                               subject="Confirmation de réception de votre commande")
            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Fraiseuse Numérique", )
            return fraiseuse_numerique(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return fraiseuse_numerique(request, errors=1, errors_txt=errors)

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

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(request = request, Service_name="Découpe Laser",
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                img_path=design_path,
                                                comment=request.POST.get('special_instructions'),
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service="Découpe Laser", obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               img_path=design_path,
                                               colors=None,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")
            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Découpe Laser", )
            return decoupe_laser(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return decoupe_laser(request, errors=1, errors_txt=errors)

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

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(request = request, Service_name='Impression 3D',
                                                obj=request.POST.get('impression_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                colors=request.POST.get('codeCouleur').split(','),
                                                img_path=design_path,
                                                comment=request.POST.get('special_instructions'),
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service="Impression 3D", obj=request.POST.get('impression_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               colors=request.POST.get('codeCouleur').split(','),
                                               img_path=design_path,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Impression 3D", )

            return impression_3D(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return impression_3D(request, errors=1, errors_txt=errors)

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

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(request = request, Service_name='Impression Textile',
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                comment=request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver,
                                                colors=request.POST.get('codeCouleur').split(','))

            msg_body2 = get_msg_for_admin_mail(request=request, service='Impression Textile',
                                               obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantite=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               msg_deliver=msg_deliver,
                                               img_path=design_path,
                                               colors=request.POST.get('codeCouleur').split(','),
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))
            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Impression Textile", )

            return impression_num_textile(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")

        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return impression_num_textile(request, errors=1, errors_txt=errors)

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

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(request = request, Service_name='Impression Papier',
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                comment=request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver,
                                                colors=request.POST.get('codeCouleur').split(','))

            msg_body2 = get_msg_for_admin_mail(request=request, service='Impression Papier',
                                               obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantite=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               msg_deliver=msg_deliver,
                                               colors=request.POST.get('codeCouleur').split(','),
                                               img_path=design_path,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Impression Papier", )

            return impression_num_papiers(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")
        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return impression_num_papiers(request, errors=1, errors_txt=errors)

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

            if not request.POST.get('upload_design_picture'):
                design_path = request.POST.get('design_picture')
            else:
                design_path = request.build_absolute_uri(order.upload_design_picture.url)

            # envoi d'un email
            if request.POST.get('delivery_mode') == "Retrait sur place Dakar":
                msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

            else:
                msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('town')}</span>, via notre service de livraison.
                Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

            msg_body1 = get_msg_for_client_mail(request = request, Service_name='Impression Objets',
                                                obj=request.POST.get('service_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                comment=request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver,
                                                colors=request.POST.get('codeCouleur').split(','))

            msg_body2 = get_msg_for_admin_mail(request=request, service='Impression Objets',
                                               obj=request.POST.get('service_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantite=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               msg_deliver=msg_deliver,
                                               colors=request.POST.get('codeCouleur').split(','),
                                               img_path=design_path,
                                               name=request.POST.get('name'),
                                               email=request.POST.get('email'),
                                               tel_number=request.POST.get('tel_number'),
                                               town=request.POST.get('town'))

            mail_to_the_client(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, msg_txt=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.POST.get('email'), 'name':request.POST.get('name')}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Impression Objets", )

            return impression_num_objects(request, errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")
        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return impression_num_objects(request, errors=1, errors_txt=errors)

