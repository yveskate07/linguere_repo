from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart
from .models import Fab_User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate

@receiver(post_save, sender=Fab_User)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'cart'):
        Cart.objects.create(user=instance)

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    if sender.name != "Users":  # évite de s'exécuter pour chaque app
        return

    # Exemple : Création du groupe
    group, created = Group.objects.get_or_create(name="Admins")

    if created:
        print("Groupe 'Admins' créé.")
    else:
        print("Groupe 'Admins' existant récupéré.")

    code_names = ['change_activity', 'view_activity', 'add_activitygalerieimage','change_activitygalerieimage',
                  'delete_activitygalerieimage','view_activitygalerieimage','add_impact','change_impact',
                  'delete_impact','view_impact','add_realisation','change_realisation','delete_realisation',
                  'view_realisation','add_resultat','change_resultat','delete_resultat','view_resultat',
                  'change_formations','view_formations','delete_galerieimageforservice','view_galerieimageforservice',
                  'change_service','view_service','change_invoice','view_invoice','view_order','add_product','change_product',
                  'view_product','add_fab_user','delete_fab_user','view_fab_user','add_feature','change_feature','delete_feature',
                  'view_feature','add_partner','change_partner','delete_partner','view_partner','add_askedquestions','change_askedquestions',
                  'delete_askedquestions','view_askedquestions']
    
    # Charger toutes les permissions en une seule fois
    perms = Permission.objects.filter(codename__in=code_names)

    existing_codenames = set(perms.values_list("codename", flat=True))
    missing = set(code_names) - existing_codenames

    special_field_perms = [{'codename':'edit_Activities_activity_name', 'name':'Can edit Activity name', 'app_label':'Activities', 'model': 'activity'}, 
                           {'codename':'edit_Activities_activity_url_name', 'name':'Can edit Activity url name', 'app_label':'Activities', 'model': 'activity'}, 
                           {'codename':'edit_Formations_formation_name', 'name':'Can edit Formation name', 'app_label':'Formations', 'model': 'formations'},
                           {'codename':'edit_Formations_formation_slug', 'name':'Can edit Formation slug', 'app_label':'Formations', 'model': 'formations'},
                           {'codename':'edit_Services_service_name', 'name':'Can edit Service name', 'app_label':'Services', 'model': 'service'},
                           {'codename':'edit_Services_services_slug', 'name':'Can edit Services slug', 'app_label':'Services', 'model': 'service'}]
    
    extra_perms = []

    for obj in special_field_perms:
        try:
            perm = Permission.objects.get(codename=obj['codename'], name=obj['name'])
        except Permission.DoesNotExist:
            ctt, _ = ContentType.objects.get_or_create(app_label=obj['app_label'], model=obj['model'])
            perm = Permission.objects.create(codename=obj['codename'], name=obj['name'], content_type=ctt)
        
        
        extra_perms.append(perm)

    all_permissions = list(perms) + extra_perms

    # Ajouter celles trouvées
    for perm in all_permissions:
        group.permissions.add(perm)

    # Afficher celles manquantes
    for codename in missing:
        print(f"Permission '{codename}' introuvable.")

    print(f"Permissions mises à jour pour le groupe Admins.")