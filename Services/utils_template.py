import json

# Icônes par défaut selon le field_type ou le nom du champ
FIELD_ICONS = {
    'select':     'fas fa-list',
    'text':       'fas fa-pen',
    'integer':    'fas fa-hashtag',
    'file':       'fas fa-file-upload',
    'boolean':    'fas fa-toggle-on',
    'multicolor': 'fas fa-palette',
}

# Icônes pour les champs communs
COMMON_ICONS = {
    'width':    'fas fa-ruler-combined',
    'height':   'fas fa-ruler-combined',
    'quantity': 'fas fa-boxes-stacked',
    'comment':  'fas fa-clipboard-list',
}


def build_input_ids_json(service_fields):
    """
    Génère le JSON attendu par le JS de résumé dynamique dans le template.

    Format de chaque item :
    {
        "input_ids": ["id_field_name"],         # un seul élément en général
        "sum_cls":   "fas fa-palette",          # icône Font Awesome
        "sum_tit_cls": "Label du champ",        # titre affiché dans le résumé
        "type": "multicolor"                    # optionnel, pour les couleurs
    }

    Cas spéciaux :
    - width + height → un seul item avec deux input_ids pour afficher "X cm × Y cm"
    - multicolor     → type="multicolor" pour que le JS utilise le color picker
    - select has_other → input_ids a deux éléments [main_id, other_id]
    """
    items = []

    # 1. Champs dynamiques spécifiques au service
    for sf in service_fields:
        icon = FIELD_ICONS.get(sf.field_type, 'fas fa-pen')
        field_id = f'id_{sf.name}'

        if sf.field_type == 'multicolor':
            items.append({
                'input_ids': [field_id],
                'sum_cls':   icon,
                'sum_tit_cls': sf.label,
                'type': 'multicolor',
            })
        elif sf.field_type == 'select' and sf.has_other:
            items.append({
                'input_ids': [field_id, f'id_{sf.name}_other'],
                'sum_cls':   icon,
                'sum_tit_cls': sf.label,
            })
        else:
            items.append({
                'input_ids': [field_id],
                'sum_cls':   icon,
                'sum_tit_cls': sf.label,
            })

    # 2. Champs communs : dimensions (width + height groupés), quantité, commentaire
    items.append({
        'input_ids':   ['id_width', 'id_height'],
        'sum_cls':     COMMON_ICONS['width'],
        'sum_tit_cls': 'Dimensions',
    })
    items.append({
        'input_ids':   ['id_quantity'],
        'sum_cls':     COMMON_ICONS['quantity'],
        'sum_tit_cls': 'Quantité',
    })
    items.append({
        'input_ids':   ['id_comment'],
        'sum_cls':     COMMON_ICONS['comment'],
        'sum_tit_cls': 'Instructions spéciales',
    })

    return json.dumps(items)