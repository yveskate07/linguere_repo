import json
from django import forms


# ==============================================================================
# CHAMPS COMMUNS : présents dans tous les formulaires de service
# ==============================================================================

DELIVERIES = [
    ('', '-- Choisir un mode de livraison --'),
    ('Retrait sur place (Dakar)',            'Retrait sur place (Dakar)'),
    ('Livraison à domicile (Dakar)',          'Livraison à domicile (Dakar)'),
    ('Livraison à domicile (Autres régions)', 'Livraison à domicile (Autres régions)'),
]

COMMON_FIELDS = {
    'quantity': forms.IntegerField(
        label='Quantité',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    ),
    'width': forms.IntegerField(
        label='Largeur (en cm)',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    ),
    'height': forms.IntegerField(
        label='Hauteur (en cm)',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    ),
    'delivery_mode': forms.ChoiceField(
        label='Mode de livraison',
        choices=DELIVERIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    ),
    'comment': forms.CharField(
        label='Instructions spéciales',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    ),
    'client_address': forms.CharField(
        label='Votre adresse',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    ),
    'img_path': forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    ),
    'img': forms.ImageField(
        label='Ajouter une image de référence',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'display:none;', 'accept': 'image/*'})  # caché, le JS gère l'affichage et la prévisualisation
    )
}

ANONYMOUS_FIELDS = {
    'client_name': forms.CharField(
        label='Votre nom complet',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    ),
    'client_email': forms.EmailField(
        label='Votre adresse email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    ),
    'client_phone': forms.CharField(
        label='Votre numéro de téléphone',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    ),
}


# ==============================================================================
# CORRESPONDANCE field_type → champ Django
# ==============================================================================

def build_field_from_service_field(service_field):
    """
    Convertit un objet ServiceField en champ Django correspondant.
    Retourne un dict {field_name: form_field} car un ServiceField de type
    'select' avec has_other=True génère deux champs Django.
    """
    ft = service_field.field_type
    name = service_field.name
    label = service_field.label
    required = service_field.required
    result = {}

    if ft == 'text':
        result[name] = forms.CharField(
            label=label,
            required=required,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    elif ft == 'integer':
        result[name] = forms.IntegerField(
            label=label,
            required=required,
            min_value=1,
            widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
        )

    elif ft == 'boolean':
        result[name] = forms.BooleanField(
            label=label,
            required=False,  # un BooleanField Django est toujours non-requis
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )

    elif ft == 'file':
        result[name] = forms.ImageField(
            label=label,
            required=required,
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )

    elif ft == 'select':
        raw_choices = service_field.choices or []
        choices = [('', f'-- {label} --')] + [(c, c) for c in raw_choices]
        result[name] = forms.ChoiceField(
            label=label,
            choices=choices,
            required=required,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        # Si "Autre (Préciser)" est une option, on ajoute un champ texte libre
        if service_field.has_other:
            result[f'{name}_other'] = forms.CharField(
                label=f'Précisez (si autre)',
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    # data-attribute pour que le JS puisse afficher/masquer ce champ
                    'data-other-for': name,
                    'placeholder': 'Précisez votre choix',
                    'style': 'display:none;'
                })
            )

    elif ft == 'multicolor':
        # Champ caché : la valeur est injectée par le JS du color picker
        # sous forme de JSON sérialisé : '["#FF0000", "#0000FF"]'
        result[name] = forms.CharField(
            label=label,
            required=required,
            widget=forms.HiddenInput(attrs={'id': f'id_{name}', 'data-type': 'multicolor'})
        )

    return result


# ==============================================================================
# GÉNÉRATEUR DE FORMULAIRE DYNAMIQUE
# ==============================================================================

def build_dynamic_form(service_fields, anonymous=False):
    """
    Construit et retourne une classe de formulaire Django dynamiquement,
    à partir des ServiceField d'un service donné.

    - Les champs communs (quantité, dimensions, livraison, commentaire)
      sont toujours inclus.
    - Les champs anonymes (nom, email, téléphone, adresse) sont inclus
      seulement si anonymous=True.
    - Les champs spécifiques au service sont ajoutés dans l'ordre défini
      par ServiceField.order.

    Utilisation :
        DynamicForm = build_dynamic_form(service.fields.all(), anonymous=True)
        form = DynamicForm(request.POST, request.FILES)
    """
    # 1. Champs communs
    declared_fields = dict(COMMON_FIELDS)

    # 2. Champs anonymes si l'utilisateur n'est pas connecté
    if anonymous:
        declared_fields.update(ANONYMOUS_FIELDS)

    # 3. Champs dynamiques spécifiques au service
    for sf in service_fields:
        declared_fields.update(build_field_from_service_field(sf))

    # 4. Construction dynamique de la classe Form
    DynamicServiceForm = type(
        'DynamicServiceForm',
        (forms.BaseForm,),
        {'base_fields': declared_fields}
    )

    return DynamicServiceForm