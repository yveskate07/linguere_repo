import re
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import ServiceInfo
from django.contrib import messages
from .tasks import mail_to_the_client, mail_to_fablab


def get_context_for_user_mail(Service_name, obj, width, height, quantite, comment, msg_deliver, img_path=None, colors=None, request=None):

    if colors:
        colors = [i.lstrip('#') for i in colors]

    context={'Service_name':Service_name,'obj':obj,'width':width,'height':height,'quantite':quantite,'comment':comment,'img_path':img_path,'msg_deliver':msg_deliver,'colors_list':colors}

    return context

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
    """with open("code2.html",'w') as f:
        f.write(msg_body)"""

    return msg_body

# Create your views here.
@login_required
def serviceView(request, slug=None, errors_txt=None, errors=0, success=0, success_txt=None):

    if not slug:
        return redirect('home')
    try:
        service = Service.objects.get(slug=slug)
    except Service.DoesNotExist:
        return render(request, 'error/index.html', context={'error_msg':"Le service que vous essayez de personnaliser n'existe pas"})
    else:
        customized_service_form = CustomizedServiceForm()

        is_colored_customization = any([field.is_color_field() for field in service.html_fields.all()])

        context = {'html_fields':service.html_fields.all(),
                'customization_form': customized_service_form,
                'slug': slug,
                'is_colored_customization': is_colored_customization,
                'serviceId': service.pk,
                'serviceName': service.name,
                'serviceDesc': service.description,
                'user_id': request.user.id,
                'img_urls': [image.image.url for image in
                                service.galerie_images.all()] if service.galerie_images.all() else None,
                'errors': errors, 'errors_txt': errors_txt, 'success': success, 'success_txt': success_txt}
        
        return render(request, "Services/index.html", context=context)

@login_required
def custom_view(request):
    print("Form datas : ", request.POST)
    if request.method == 'POST':
        form = CustomizedServiceForm(data=request.POST, files=request.FILES)
        try:
            print("Fetching service...")
            service = Service.objects.get(slug=request.POST.get("slug"))
        except Service.DoesNotExist:
            print("Service does not exist")
            return render(request, 'error/index.html', context={'error_msg':"Le service que vous essayez de personnaliser n'existe pas"})
        else:
            if form.is_valid():
                print("Form is valid")
                subs_user = form.save(commit=False)
                if request.POST.get('imported_picture', False):
                    print("picture is imported")
                    subs_user.imported_picture = request.FILES.get('imported_picture')
                    subs_user.save()
                    design_path = request.build_absolute_uri(subs_user.imported_picture.url)
                else:
                    print("picture is chosen")
                    subs_user.chosen_picture = request.POST.get('chosen_picture','')
                    subs_user.save()
                    design_path = subs_user.chosen_picture

                fields_dict = {}
                for field in service.html_fields.all():
                    fields_dict[field.get_input_name] = request.POST.get(field.get_input_name, None)

                subs_user.fields_value = fields_dict
                
                subs_user.user = request.user
                subs_user.service = service
                subs_user.save()

                if request.POST.get('delivery_mode') == "Retrait sur place (Dakar)":
                    msg_deliver = """Nous vous tiendrons informé dès que la commande sera prête pour que vous passiez la retirer."""

                else:
                    msg_deliver = f"""La livraison s’effectuera à l’adresse suivante : <span class="highlight">{request.POST.get('adress_delivery')}</span>, via notre service de livraison.
                    Nous vous tiendrons informé dès que la commande sera expédiée, accompagnée des détails de suivi."""

                # ces names devront etre respectés lorsque les html_fields seront créés
                colors=request.POST.get('codeCouleur',None)
                if colors:
                    colors = colors.split(',')

                support_field = service.get_support_field_name
                if isinstance(support_field, list):
                    for name in support_field:
                        if request.POST.get(name, False):
                            support = request.POST.get(name)
                            break
                else:
                    support = request.POST.get(support_field)

                ctx = get_context_for_user_mail(request = request, Service_name=service.name,
                                                    obj=support, 
                                                    width=request.POST.get('dim_1'),
                                                    height=request.POST.get('dim_2'),
                                                    quantite=request.POST.get('quantity'),
                                                    colors=colors,
                                                    comment = request.POST.get('special_instructions'),
                                                    img_path=design_path,
                                                    msg_deliver=msg_deliver)
                
                """mail_to_the_client(user={'e-mail': request.user.email, 'name':request.user.name}
                                   , context=ctx, is_formation=False, formation_name=service.name)"""

                """mail_to_fablab(user={'e-mail': request.user.email, 'name':request.user.name},
                               admin_edit_view = f"/admin/Services/customizedservice/{subs_user.pk}/change/", 
                               is_formation=False, 
                               formation_name=service.name, 
                               reason="new service order")"""

                return serviceView(request, slug=request.POST.get('slug'), errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")
            
            else:
                print("Form is invalid")
                errors = list(form.errors.values())
                errors = [error[0] for error in errors]
                return serviceView(request, slug=request.POST.get('slug'), errors=1, errors_txt=errors)

def sending_mail(request, instance_order, service):
    try:
        colors_list = [item.color for item in instance_order.selected_colors.all()]
    except AttributeError:
        colors_list = None

    context = {"subject": "Nouvelle commande de service enregistrée", "Service_name":service, "obj": instance_order.get_obj(), "width":instance_order.width, 
               "height":instance_order.height, "quantite":instance_order.quantity, 
               "colors_list": colors_list, "comment":instance_order.comment, 
               "img_path":instance_order.get_img_path(), "deliver":instance_order.delivery_mode, "name":instance_order.client_name, 
               "email":instance_order.client_email, "tel_number":instance_order.client_phone , "town":instance_order.client_address,
               "admin_edit_view":f"/admin/Services/{instance_order._meta.model_name}/{instance_order.pk}/change/"}
    
    msg_admin = render_to_string(request=request, template_name='Services/mail_for_fablab/index.html', context=context)
    msg_client = render_to_string(request=request, template_name='Services/mail_for_users/index.html', context=context)

    with open("admin_code.html",'w') as f:
        f.write(msg_admin)

    with open("client_code.html",'w') as f:
        f.write(msg_client)

    #mail_to_fablab(msg=msg)

    #mail_to_the_client(user_email=instance_order.client_email, msg=msg)

def checking_slug(request, slug):
    if slug == "broderie-numerique":
        return brod_num_view(request)
    elif slug == "decoupe-et-gravure-laser":
        return dec_grav_laser_view(request)
    elif slug == "service-de-fraiseuse-numerique-cnc":
        return fraiseuse_cnc_view(request)
    elif slug == "service-dimpression-3d":  
        return impression_3d_view(request)
    elif slug == "impression-sur-objets-personnalises":
        return impression_objets_personnalises_view(request)
    elif slug == "impression-sur-papier-et-supports-rigides":
        return impression_papier_supports_rigides_view(request)
    elif slug == "impression-sur-textiles-et-vetements":
        return impression_textiles_vetements_view(request)
    else:
        return redirect('home')


def brod_num_view(request):
    if not request.method == "POST":
        try:
            service = ServiceInfo.objects.get(name="Broderie Numérique")
            img_urls = [image.image.url for image in service.galerie_images.all()]
            if request.user.is_authenticated:
                user_id = request.user.id
                serviceCustomisation = BroderieNumeriqueModelForm()
            else:
                user_id = 'anonymous_id'
                serviceCustomisation = AnonymousBroderieNumeriqueModelForm()
        except ServiceInfo.DoesNotExist:
            return redirect('home')
        else:
            # retrieving service form
            return render(request, 'Services/brod_num/index.html', context={'service':service, 'user_id': user_id, 
                                                                            'serviceCustomisation':serviceCustomisation,
                                                                'img_urls': img_urls})
    else:
        if not request.user.is_authenticated:
            form = AnonymousBroderieNumeriqueModelForm(data=request.POST, files=request.FILES)
        else:
            form = BroderieNumeriqueModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.img_path = request.POST.get('img_path')

            colors = request.POST.get('selected-colors').split(',')
            if request.user.is_authenticated:
                order.client_name = request.user.first_name + " " + request.user.last_name
                order.client_email = request.user.email
                order.client_phone = request.user.tel_num
            else:
                order.client_name = request.POST.get('client_name')
                order.client_email = request.POST.get('client_email')
                order.client_phone = request.POST.get('client_phone')

            order.save()
            for hexacode in colors:
                color = Colors.objects.create(service=order, color=hexacode)

            # notifying by mail both client and admins for this order
            sending_mail(request, instance_order=order, service="Broderie Numérique")
            messages.success(request,"Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail.")
            return redirect('service', slug="broderie-numerique")

        else:
            print(form.errors)
            return redirect('home')
                

def dec_grav_laser_view(request):
    if not request.method == "POST":
        try:
            service = ServiceInfo.objects.get(name="Découpe et Gravure Laser")
            img_urls = [image.image.url for image in service.galerie_images.all()]
            if request.user.is_authenticated:
                user_id = request.user.id
                serviceCustomisation = DecoupeLaserModelForm()
            else:
                user_id = 'anonymous_id'
                serviceCustomisation = AnonymousDecoupeLaserModelForm()
        except ServiceInfo.DoesNotExist:
            return redirect('home')
        else:
            # retrieving service form
            return render(request, 'Services/laser/index.html', context={'service':service, 'user_id': user_id, 
                                                                            'serviceCustomisation':serviceCustomisation,
                                                                            'img_urls': img_urls})
    else:
        if not request.user.is_authenticated:
            form = AnonymousDecoupeLaserModelForm(data=request.POST, files=request.FILES)
        else:
            form = DecoupeLaserModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.img_path = request.POST.get('img_path')

            if request.user.is_authenticated:
                order.client_name = request.user.first_name + " " + request.user.last_name
                order.client_email = request.user.email
                order.client_phone = request.user.tel_num
            else:
                order.client_name = request.POST.get('client_name')
                order.client_email = request.POST.get('client_email')
                order.client_phone = request.POST.get('client_phone')

            order.save()

            # notifying by mail both client and admins for this order
            sending_mail(request, instance_order=order, service="Découpe et Gravure Laser")
            messages.success(request,"Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail.")
            return redirect('service', slug="decoupe-et-gravure-laser")

        else:
            print(form.errors)
            return redirect('home')


def fraiseuse_cnc_view(request):
    if not request.method == "POST":
        try:
            service = ServiceInfo.objects.get(name="Service de Fraiseuse Numérique CNC")
            img_urls = [image.image.url for image in service.galerie_images.all()]
            if request.user.is_authenticated:
                user_id = request.user.id
                serviceCustomisation = FraiseCNCModelForm()
            else:
                user_id = 'anonymous_id'
                serviceCustomisation = AnonymousFraiseCNCModelForm()
        except ServiceInfo.DoesNotExist:
            return redirect('home')
        else:
            # retrieving service form
            return render(request, 'Services/frais_num/index.html', context={'service':service, 'user_id': user_id, 
                                                                            'serviceCustomisation':serviceCustomisation,
                                                                            'img_urls': img_urls})
    else:
        if not request.user.is_authenticated:
            form = AnonymousFraiseCNCModelForm(data=request.POST, files=request.FILES)
        else:
            form = FraiseCNCModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.img_path = request.POST.get('img_path')

            if request.user.is_authenticated:
                order.client_name = request.user.first_name + " " + request.user.last_name
                order.client_email = request.user.email
                order.client_phone = request.user.tel_num
            else:
                order.client_name = request.POST.get('client_name')
                order.client_email = request.POST.get('client_email')
                order.client_phone = request.POST.get('client_phone')

            order.save()

            # notifying by mail both client and admins for this order
            sending_mail(request, instance_order=order, service="Service de Fraiseuse Numérique CNC")
            messages.success(request,"Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail.")
            return redirect('service', slug="service-de-fraiseuse-numerique-cnc")

        else:
            print(form.errors)
            return redirect('home')


def impression_3d_view(request):
    if not request.method == "POST":
        try:
            service = ServiceInfo.objects.get(name="Service d’Impression 3D")
            img_urls = [image.image.url for image in service.galerie_images.all()]
            if request.user.is_authenticated:
                user_id = request.user.id
                serviceCustomisation = Impression3DModelForm()
            else:
                user_id = 'anonymous_id'
                serviceCustomisation = AnonymousImpression3DModelForm()
        except ServiceInfo.DoesNotExist:
            return redirect('home')
        else:
            # retrieving service form
            return render(request, 'Services/serv_imp_3d/index.html', context={'service':service, 'user_id': user_id, 
                                                                            'serviceCustomisation':serviceCustomisation,
                                                                            'img_urls': img_urls})
    else:
        if not request.user.is_authenticated:
            form = AnonymousImpression3DModelForm(data=request.POST, files=request.FILES)
        else:
            form = Impression3DModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.img_path = request.POST.get('img_path')

            colors = request.POST.get('selected-colors').split(',')
            if request.user.is_authenticated:
                order.client_name = request.user.first_name + " " + request.user.last_name
                order.client_email = request.user.email
                order.client_phone = request.user.tel_num
            else:
                order.client_name = request.POST.get('client_name')
                order.client_email = request.POST.get('client_email')
                order.client_phone = request.POST.get('client_phone')

            order.save()
            for hexacode in colors:
                color = Colors.objects.create(service=order, color=hexacode)

            # notifying by mail both client and admins for this order
            sending_mail(request, instance_order=order, service="Service d’Impression 3D")
            messages.success(request,"Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail.")
            return redirect('service', slug="service-d-impression-3d")

        else:
            print(form.errors)
            return redirect('home')


def impression_objets_personnalises_view(request):
    if not request.method == "POST":
        try:
            service = ServiceInfo.objects.get(name="Impression sur Objets Personnalisés")
            img_urls = [image.image.url for image in service.galerie_images.all()]
            if request.user.is_authenticated:
                user_id = request.user.id
                serviceCustomisation = ImpressionObjPersonnaliseModelForm()
            else:
                user_id = 'anonymous_id'
                serviceCustomisation = AnonymousImpressionObjPersonnaliseModelForm()
        except ServiceInfo.DoesNotExist:
            return redirect('home')
        else:
            # retrieving service form
            return render(request, 'Services/imp_obj_pers/index.html', context={'service':service, 'user_id': user_id, 
                                                                            'serviceCustomisation':serviceCustomisation,
                                                                            'img_urls': img_urls})
    else:
        if not request.user.is_authenticated:
            form = AnonymousImpressionObjPersonnaliseModelForm(data=request.POST, files=request.FILES)
        else:
            form = ImpressionObjPersonnaliseModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.img_path = request.POST.get('img_path')

            colors = request.POST.get('selected-colors').split(',')
            if request.user.is_authenticated:
                order.client_name = request.user.first_name + " " + request.user.last_name
                order.client_email = request.user.email
                order.client_phone = request.user.tel_num
            else:
                order.client_name = request.POST.get('client_name')
                order.client_email = request.POST.get('client_email')
                order.client_phone = request.POST.get('client_phone')

            order.save()
            for hexacode in colors:
                color = Colors.objects.create(service=order, color=hexacode)

            # notifying by mail both client and admins for this order
            sending_mail(request, instance_order=order, service="Impression sur Objets Personnalisés")
            messages.success(request,"Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail.")
            return redirect('service', slug="impression-sur-objets-personnalises")

        else:
            print(form.errors)
            return redirect('home')


def impression_papier_supports_rigides_view(request):
    if not request.method == "POST":
        try:
            service = ServiceInfo.objects.get(name="Impression sur Papier et Supports Rigides")
            img_urls = [image.image.url for image in service.galerie_images.all()]
            if request.user.is_authenticated:
                user_id = request.user.id
                serviceCustomisation = ImpressionPaperSupportRigideModelForm()
            else:
                user_id = 'anonymous_id'
                serviceCustomisation = AnonymousImpressionPaperSupportRigideModelForm()
        except ServiceInfo.DoesNotExist:
            return redirect('home')
        else:
            return render(request, 'Services/imp_pap_sup_rig/index.html', context={'service':service, 'user_id': user_id, 
                                                                            'serviceCustomisation':serviceCustomisation,
                                                                            'img_urls': img_urls})
    else:
        if not request.user.is_authenticated:
            form = AnonymousImpressionPaperSupportRigideModelForm(data=request.POST, files=request.FILES)
        else:
            form = ImpressionPaperSupportRigideModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.img_path = request.POST.get('img_path')

            colors = request.POST.get('selected-colors').split(',')
            if request.user.is_authenticated:
                order.client_name = request.user.first_name + " " + request.user.last_name
                order.client_email = request.user.email
                order.client_phone = request.user.tel_num
            else:
                order.client_name = request.POST.get('client_name')
                order.client_email = request.POST.get('client_email')
                order.client_phone = request.POST.get('client_phone')

            order.save()
            for hexacode in colors:
                color = Colors.objects.create(service=order, color=hexacode)

            # notifying by mail both client and admins for this order
            sending_mail(request, instance_order=order, service="Impression sur Papier et Supports Rigides")
            messages.success(request,"Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail.")
            return redirect('service', slug="impression-sur-papier-et-supports-rigides")

        else:
            print(form.errors)
            return redirect('home')


def impression_textiles_vetements_view(request):
    if not request.method == "POST":
        try:
            service = ServiceInfo.objects.get(name="Impression sur Textiles et Vêtements")
            img_urls = [image.image.url for image in service.galerie_images.all()]
            if request.user.is_authenticated:
                user_id = request.user.id
                serviceCustomisation = ImpressionTextileEtVetementModelForm()
            else:
                user_id = 'anonymous_id'
                serviceCustomisation = AnonymousImpressionTextileEtVetementModelForm()
        except ServiceInfo.DoesNotExist:
            return redirect('home')
        else:
            return render(request, 'Services/imp_text_vet/index.html', context={'service':service, 'user_id': user_id, 
                                                                            'serviceCustomisation':serviceCustomisation,
                                                                            'img_urls': img_urls})
    else:
        if not request.user.is_authenticated:
            form = AnonymousImpressionTextileEtVetementModelForm(data=request.POST, files=request.FILES)
        else:
            form = ImpressionTextileEtVetementModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.img_path = request.POST.get('img_path')

            colors = request.POST.get('selected-colors').split(',')
            if request.user.is_authenticated:
                order.client_name = request.user.first_name + " " + request.user.last_name
                order.client_email = request.user.email
                order.client_phone = request.user.tel_num
            else:
                order.client_name = request.POST.get('client_name')
                order.client_email = request.POST.get('client_email')
                order.client_phone = request.POST.get('client_phone')

            order.save()
            for hexacode in colors:
                color = Colors.objects.create(service=order, color=hexacode)

            # notifying by mail both client and admins for this order
            sending_mail(request, instance_order=order, service="Impression sur Textiles et Vêtements")
            messages.success(request,"Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail.")
            return redirect('service', slug="impression-sur-textiles-et-vetements")

        else:
            print(form.errors)
            return redirect('home')
