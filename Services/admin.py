from django.contrib import admin
from Services.models import GalerieImageForService, Service, ServiceField, ServiceOrder, ServiceOrderFieldValue


class ServiceFieldInline(admin.TabularInline):
    model = ServiceField
    extra = 0
    can_delete = False  # Empêche la suppression des champs via l'interface admin
    

    def has_delete_permission(self, request, obj = ...):

        return request.user.groups.filter(name='Developpers').exists()

    def has_change_permission(self, request, obj=None):
        # Seuls les utilisateurs du groupe "Developpers" peuvent modifier les champs
        # return request.user.groups.filter(name='Developpers').exists()
        return False

    """def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        # Affiche ou masque la case "Supprimer"
        formset.can_delete = request.user.groups.filter(
            name='Developpers'
        ).exists()

        return formset"""


class ServiceOrderFieldValueInline(admin.TabularInline):
    model = ServiceOrderFieldValue
    fields = ('field', 'colored_value')
    readonly_fields = ('field', 'colored_value')
    extra = 0
    can_delete = False  # Empêche la suppression des champs via l'interface admin


    def has_delete_permission(self, request, obj = ...):

        return request.user.groups.filter(name='Developpers').exists()

    def has_change_permission(self, request, obj=None):
        # Seuls les utilisateurs du groupe "Developpers" peuvent modifier les champs
        # return request.user.groups.filter(name='Developpers').exists()
        return False

    """def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        # Affiche ou masque la case "Supprimer"
        formset.can_delete = request.user.groups.filter(
            name='Developpers'
        ).exists()

        return formset"""
        

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
     fields = ('service', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address')
     list_display = ('service', 'created_at', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address')
     inlines = [ServiceOrderFieldValueInline]


class GalerieImageForServiceInline(admin.TabularInline):
    model = GalerieImageForService
    extra = 0

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [GalerieImageForServiceInline, ServiceFieldInline]
    list_display = ('name',)
    fields = ('name', 'description', 'description_accueil','slug',)

    class Media:
        js = ('Services/js/admin/services.js',)  # Assurez-vous que ce chemin est correct et que le fichier existe

