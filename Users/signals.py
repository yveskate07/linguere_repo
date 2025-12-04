from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart
from .models import Fab_User
#from django.contrib.auth.models import Permission

@receiver(post_save, sender=Fab_User)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'cart'):
        Cart.objects.create(user=instance)

"""
@receiver(post_save, sender=Fab_User)
def restrict_group_permission(sender, instance, **kwargs):
    if not instance.is_superuser:
        perm = Permission.objects.get(
            codename="view_group",
            content_type__app_label="auth",
            content_type__model="group"
        )
        instance.user_permissions.remove(perm)
        instance.save()"""