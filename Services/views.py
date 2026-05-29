import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from .tasks import mail_to_fablab, mail_to_the_client, double_nombre
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

    Pour chaque ServiceField :
    - 'multicolor' : la valeur vient du POST (JSON sérialisé par le JS),
                     on vérifie que c'est du JSON valide avant de sauver.
    - 'file'       : le fichier est dans request.FILES, on sauve l'URL après upload.
    - 'select' avec has_other : si la valeur est "Autre (Préciser)", on prend
                                la valeur du champ *_other à la place.
    - Autres types : on prend directement cleaned_data.
    """
    for sf in service_fields:
        value = ''

        if sf.field_type == 'multicolor':
            raw = cleaned_data.get(sf.name, '[]')
            try:
                parsed = json.loads(raw)
                value = json.dumps(parsed)   # re-sérialise proprement
            except (ValueError, TypeError):
                value = '[]'

        elif sf.field_type == 'file':
            uploaded = request.FILES.get(sf.name)
            if uploaded:
                # On lie le fichier uploadé à l'image principale de la commande
                # pour réutiliser le champ ImageField déjà défini sur ServiceOrder.
                # Si plusieurs champs de type file existent, seul le premier
                # sera stocké dans order.image ; les suivants seront dans value.
                if not order.image:
                    order.image = uploaded
                    order.save(update_fields=['image'])
                    value = order.image.url
                else:
                    # Cas rare : second fichier uploadé → stocker le chemin brut
                    value = uploaded.name
        elif sf.field_type == 'file_path':
            img_path = cleaned_data.get(sf.name, '')
            value = img_path if img_path else ''

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


# ==============================================================================
# VUE UNIQUE — gère GET et POST pour tous les services
# ==============================================================================

def service_view(request, slug):
    """
    Vue unique pour tous les services de personnalisation.

    GET  → affiche la page du service avec son formulaire dynamique.
    POST → valide le formulaire, crée la commande, envoie le mail de confirmation.

    Le formulaire est construit dynamiquement à partir des ServiceField
    associés au service (définis par le client dans l'admin Django).
    """

    # --- Récupération du service ---
    service = get_object_or_404(Service, slug=slug)
    service_fields = service.fields.order_by('order')
    multicolor_fields = set(sf.name for sf in service_fields if sf.field_type == 'multicolor')
    img_urls = [image.image.url for image in service.galerie_images.all()]
    anonymous = not request.user.is_authenticated

    # --- Classe de formulaire dynamique ---
    DynamicForm = build_dynamic_form(service_fields, anonymous=anonymous)

    # ------------------------------------------------------------------
    # GET : affichage du formulaire vide
    # ------------------------------------------------------------------
    input_ids_json = build_input_ids_json(service_fields)


    if request.method != 'POST':
        form = DynamicForm()
        return render(request, 'Services/index.html', {
            'service':        service,
            'service_fields': service_fields,
            'form':           form,
            'img_urls':       img_urls,
            'multicolor_fields': multicolor_fields,
            'input_ids_json': input_ids_json,
        })

    # ------------------------------------------------------------------
    # POST : traitement du formulaire soumis
    # ------------------------------------------------------------------
    form = DynamicForm(data=request.POST, files=request.FILES)

    if not form.is_valid():
        return render(request, 'Services/index.html', {
            'service':        service,
            'service_fields': service_fields,
            'form':           form,
            'img_urls':       img_urls,
            'multicolor_fields': multicolor_fields,
            'input_ids_json': input_ids_json,
        })

    cd = form.cleaned_data

    # 1. Créer la commande avec les champs communs
    order = ServiceOrder(
        service=service,
        quantity=cd.get('quantity'),
        width=cd.get('width'),
        height=cd.get('height'),
        delivery_mode=cd.get('delivery_mode', ''),
        comment=cd.get('comment', ''),
    )

    # 2. Remplir les infos client
    _populate_client_info(order, request)

    # 3. Sauvegarder la commande (sans l'image pour l'instant)
    order.save()

    # 4. Sauvegarder les valeurs des champs dynamiques
    #    (y compris l'image si un champ de type 'file' existe)
    _save_dynamic_field_values(order, service_fields, cd, request)

    # 5. Envoyer les mails de confirmation
    #    (ta fonction sending_mail existante — on lui passe l'order)
    try:
        mail_to_the_client.delay(order.client_email, f"Votre commande #{order.pk} a été enregistrée avec succès.")
        mail_to_fablab.delay(f"Nouvelle commande #{order.pk} pour le service '{service.name}' enregistrée. Client : {order.client_name}, Email : {order.client_email}.")
    except Exception as e:
        # On ne bloque pas la commande si l'envoi mail échoue
        print(f"[WARNING] Envoi mail échoué pour commande #{order.pk} : {e}")
    
    messages.success(
        request,
        "Votre commande a bien été enregistrée. Veuillez consulter votre boîte mail."
    )
    return redirect('service', slug=slug)