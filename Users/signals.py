"""from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Permission
from .models import Fab_User


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