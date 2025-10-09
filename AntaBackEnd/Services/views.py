import json
import re

from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Services.forms import CustomizedServiceForm
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
def serviceView(request, slug=None, errors_txt=None, errors=0, success=0, success_txt=None):
    if not slug:
        return redirect('home')
    service = Service.objects.get(slug=slug)
    customized_service_form = CustomizedServiceForm()
    fields_names = [{'is_grouped':field.grouped, 'field_name': field.get_input_name, 'header_class':field.header_icon_class, 'header_txt':field.header_icon_txt} for field in service.html_fields.all()]

    is_colored_customization = any([field.is_color_field() for field in service.html_fields.all()])

    context = {'html_fields':service.html_fields.all(),
               'customization_form': customized_service_form,
               'fields_names_js': fields_names,
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
    print(f'request.POST : {request.POST}')
    # redirecting to facebook.com
    return redirect('https://www.facebook.com')
    if request.method == 'POST':
        form = CustomizedServiceForm(adress_delivery=request.POST.get('adress_delivery'), delivery_mode=request.POST.get('delivery_mode'), cgu_accept=request.POST.get('cgu_accept'))
        service = Service.objects.get(slug=request.POST.get("slug"))

        if form.is_valid():
            subs_user = form.save(commit=False)
            if request.POST.get('imported_picture', False):
                subs_user.imported_picture = request.FILES.get('imported_picture')
                subs_user.save()
                design_path = request.build_absolute_uri(subs_user.imported_picture.url)
            else:
                subs_user.chosen_picture = request.POST.get('chosen_picture','')
                subs_user.save()
                design_path = subs_user.chosen_picture

            fields_dict = {}
            for field in service.html_fields.all():
                fields_dict[field.get_input_name] = request.POST.get(field.get_input_name, '')

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

            msg_body1 = get_msg_for_client_mail(request = request, Service_name=service.name,
                                                obj=request.POST.get('support_type'),
                                                width=request.POST.get('dim_1'),
                                                height=request.POST.get('dim_2'),
                                                quantite=request.POST.get('quantity'),
                                                colors=colors,
                                                comment = request.POST.get('special_instructions'),
                                                img_path=design_path,
                                                msg_deliver=msg_deliver)

            msg_body2 = get_msg_for_admin_mail(request=request, service=service.name, obj=request.POST.get('support_type'),
                                               width=request.POST.get('dim_1'),
                                               height=request.POST.get('dim_2'),
                                               quantity=request.POST.get('quantity'),
                                               comment=request.POST.get('special_instructions'),
                                               delivery=request.POST.get('delivery_mode'),
                                               img_path=design_path,
                                               colors=colors,
                                               name=request.user.name,
                                               email=request.user.email,
                                               tel_number=request.user.tel_num,
                                               town=request.POST.get('adress_delivery'))
            
            mail_to_the_client(user={'e-mail': request.user.email, 'name':request.user.name}, html_msg=msg_body1,
                               subject="Confirmation de réception de votre commande")

            mail_to_fablab(user={'e-mail': request.user.email, 'name':request.user.name}, html_msg=msg_body2,
                           subject="Nouvelle commande enregistrée pour Broderie Numérique")

            return serviceView(request, slug=request.POST.get('slug'), errors=0, success=1, success_txt="Felicitations votre commande a été enregistrée ")
        
        else:
            errors = list(form.errors.values())
            errors = [error[0] for error in errors]
            return serviceView(request, slug=request.POST.get('slug'), errors=1, errors_txt=errors)
