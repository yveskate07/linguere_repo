import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.sites.models import Site
from django.conf import settings
from django.templatetags.static import static
from .tasks import mail_to_fablab, mail_to_the_client
from .models import Service, ServiceOrder, ServiceOrderFieldValue
from .forms import build_dynamic_form
from .utils_template import build_input_ids_json


# ==============================================================================
# UTILITAIRES
# ==============================================================================

def _populate_client_info(order, request):
    """
    Remplit les infos client sur la commande selon que
    l'utilisateur est authentifié ou non.
    """
    if request.user.is_authenticated:
        order.client_name  = f"{request.user.first_name} {request.user.last_name}".strip()
        order.client_email = request.user.email
        order.client_phone = getattr(request.user, 'tel_num', '')
    else:
        order.client_name    = request.POST.get('client_name', '')
        order.client_email   = request.POST.get('client_email', '')
        order.client_phone   = request.POST.get('client_phone', '')
    order.client_address = request.POST.get('client_address', '')


def _save_dynamic_field_values(order, service_fields, cleaned_data, request):
    
    """
    Enregistre les valeurs des champs dynamiques dans ServiceOrderFieldValue.
    """
    for sf in service_fields:
        value = ''

        if sf.field_type == 'multicolor':
            raw = cleaned_data.get(sf.name, '[]')
            try:
                parsed = json.loads(raw)
                value = json.dumps(parsed)
            except (ValueError, TypeError):
                value = '[]'

        elif sf.field_type == 'select' and sf.has_other:
            selected = cleaned_data.get(sf.name, '')
            if selected == 'Autre (Préciser)':
                value = cleaned_data.get(f'{sf.name}_other', '') or selected
            else:
                value = selected

        elif sf.field_type == 'boolean':
            value = 'true' if cleaned_data.get(sf.name) else 'false'

        else:
            raw = cleaned_data.get(sf.name, '')
            value = str(raw) if raw is not None else ''

        ServiceOrderFieldValue.objects.create(
            order=order,
            field=sf,
            value=value
        )


def _build_mail_context(order, request=None, img_upload=False):
    """
    Construit le contexte complet à passer au template du mail de confirmation.

    Pour les champs 'multicolor', la valeur est désérialisée en liste de hex
    afin que le template puisse afficher des cercles colorés.
    """
    EXCLUDED_TYPES = {'file',}

    dynamic_fields = []
    for fv in order.field_values.select_related('field').all():
        if fv.field is None:
            continue
        if fv.field.field_type in EXCLUDED_TYPES:
            continue

        if fv.field.field_type == 'multicolor':
            try:
                typed_value = json.loads(fv.value)   # liste de hex strings
            except (ValueError, TypeError):
                typed_value = []
        elif fv.field.field_type == 'boolean':
            typed_value = fv.value.lower() == 'true'
        elif fv.field.field_type == 'integer':
            try:
                typed_value = int(fv.value)
            except (ValueError, TypeError):
                typed_value = fv.value
        else:
            typed_value = fv.value

        dynamic_fields.append({
            'label':      fv.field.label,
            'value':      typed_value,
            'field_type': fv.field.field_type,
        })

        if img_upload:
            # building absolute URI for the uploaded image to be accessible in the email template
            img_link = request.build_absolute_uri(order.image.url) if order.image else ''
        else:
            img_link = order.img_path 

    return {
        'order_id':      order.pk,
        'service_name':  str(order.service) if order.service else '',
        'quantity':      order.quantity,
        'width':         order.width,
        'height':        order.height,
        'delivery_mode': order.delivery_mode,
        'comment':       order.comment or '',
        'client_name':   order.client_name,
        'dynamic_fields': dynamic_fields,
        "logo_url": request.build_absolute_uri(static('AntaBackEnd/images/logos.jpeg')) if request else '',
        "img_link": img_link,
    }


# ==============================================================================
# VUE UNIQUE — gère GET et POST pour tous les services
# ==============================================================================

def service_view(request, slug):
    """
    Vue unique pour tous les services de personnalisation.

    GET  → affiche la page du service avec son formulaire dynamique.
    POST → valide le formulaire, crée la commande, envoie le mail de confirmation.
    """

    service = get_object_or_404(Service, slug=slug)
    service_fields = service.fields.order_by('order')
    multicolor_fields = set(sf.name for sf in service_fields if sf.field_type == 'multicolor') # les names des champs multicolor pour le template
    img_urls = [image.image.url for image in service.galerie_images.all()]
    anonymous = not request.user.is_authenticated 

    DynamicForm = build_dynamic_form(service_fields, anonymous=anonymous)
    input_ids_json = build_input_ids_json(service_fields)

    # ------------------------------------------------------------------
    # GET
    # ------------------------------------------------------------------
    if request.method != 'POST':
        form = DynamicForm()
        return render(request, 'Services/index.html', {
            'service':           service,
            'service_fields':    service_fields,
            'form':              form,
            'img_urls':          img_urls,
            'multicolor_fields': multicolor_fields,
            'input_ids_json':    input_ids_json,
        })

    # ------------------------------------------------------------------
    # POST
    # ------------------------------------------------------------------
    
    form = DynamicForm(data=request.POST, files=request.FILES)

    if not form.is_valid():
        return render(request, 'Services/index.html', {
            'service':           service,
            'service_fields':    service_fields,
            'form':              form,
            'img_urls':          img_urls,
            'multicolor_fields': multicolor_fields,
            'input_ids_json':    input_ids_json,
        })

    cd = form.cleaned_data

    # 1. Créer la commande avec les champs communs
    if request.FILES:
        order = ServiceOrder(
            service=service,
            quantity=cd.get('quantity'),
            width=cd.get('width'),
            height=cd.get('height'),
            delivery_mode=cd.get('delivery_mode', ''),
            comment=cd.get('comment', ''),
            image=request.FILES.get('img')  # Champ d'upload d'image
        )
    else:
        order = ServiceOrder(
            service=service,
            quantity=cd.get('quantity'),
            width=cd.get('width'),
            height=cd.get('height'),
            delivery_mode=cd.get('delivery_mode', ''),
            comment=cd.get('comment', ''),
            img_path=cd.get('img_path', ''),
        )

    # 2. Infos client
    _populate_client_info(order, request)

    # 3. Sauvegarder la commande
    order.save()

    # 4. Sauvegarder les valeurs des champs dynamiques
    _save_dynamic_field_values(order, service_fields, cd, request)

    # 5. Construire le contexte du mail
    mail_context = _build_mail_context(order, request=request, img_upload=bool(request.FILES))

    link = request.build_absolute_uri(f"/admin/Services/serviceorder/{order.pk}/change/")

    # 6. Envoyer les mails
    try:
        mail_to_the_client.delay(
            recipient=order.client_email,
            subject="Confirmation de votre commande",
            context=mail_context,
        )
        mail_to_fablab.delay(
            user={
                'e-mail': 'linguerefablab@gmail.com',
                'message': (
                    f"Nouvelle commande #{order.pk} pour le service '{service.name}'. "
                    f"Client : {order.client_name}, Email : {order.client_email}."
                ),
            },
            subject=f"Nouvelle commande #{order.pk} - {service.name}",
            message_to_admin="Veuillez consulter les détails de la commande dans l'interface d'administration.",
            context={
                **mail_context,
                'client_email': order.client_email,
                'client_phone': order.client_phone,
                'client_address': order.client_address,
                'link': link,
            },
        )
    except Exception as e:
        print(f"[WARNING] Envoi mail échoué pour commande #{order.pk} : {e}")

    messages.success(
        request,
        "Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail."
    )
    return redirect('service', slug=slug)