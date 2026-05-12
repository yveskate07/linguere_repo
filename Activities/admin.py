from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from .models import *

if admin.site.is_registered(Group):
    admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    def has_module_permission(self, request):
        # On vérifie UNIQUEMENT le groupe, peu importe le statut superuser
        return request.user.groups.filter(name="Developpers").exists()

    def has_view_permission(self, request, obj=None):
        return request.user.groups.filter(name="Developpers").exists()

    def has_add_permission(self, request):
        return request.user.groups.filter(name="Developpers").exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name="Developpers").exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name="Developpers").exists()


class ActivityGalerieImageInline(admin.TabularInline):
    model = ActivityGalerieImage
    extra = 0

    def get_max_num(self, request, obj = ..., **kwargs):
        
        return 3

class RealisationInline(admin.TabularInline):
    model = Realisation
    extra = 0

    def get_max_num(self, request, obj = ..., **kwargs):
        
        return 3

class ResultatInline(admin.TabularInline):
    model = Resultat
    extra = 0

    def get_max_num(self, request, obj = ..., **kwargs):
        
        return 1

class ImpactInline(admin.TabularInline):
    model = Impact
    extra = 0

    def get_max_num(self, request, obj = ..., **kwargs):
        
        return 3


# Register your models here.
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    inlines = [ActivityGalerieImageInline, RealisationInline, ResultatInline, ImpactInline]
    list_display = ('name', 'created_at',)
    fields = ('name', 'description', 'description_accueil', 'presentation_img',)
    
    def get_fields(self, request, obj=None):
        if obj and request.user.groups.filter(name='Developpers').exists():
            return ('name', 'description', 'description_accueil', 'presentation_img', 'motiv1', 'motiv2','url_name',)
        
        if not request.user.has_perm('Activities.edit_Activities_activity_name'):
            return ('description', 'description_accueil', 'presentation_img', 'motiv1', 'motiv2','url_name',)
        
        return super().get_fields(request, obj)