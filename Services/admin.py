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
        return request.user.groups.filter(name='Developpers').exists()
        

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        # Affiche ou masque la case "Supprimer"
        formset.can_delete = request.user.groups.filter(
            name='Developpers'
        ).exists()

        return formset


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
        return request.user.groups.filter(name='Developpers').exists()
        

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        # Affiche ou masque la case "Supprimer"
        formset.can_delete = request.user.groups.filter(
            name='Developpers'
        ).exists()

        return formset
        

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    fields = ('service', 'quantity', 'width', 'height', 'image', 'comment', 'delivery_mode','client_name', 'client_email', 'client_phone', 'client_address')
    list_display = ('service', 'created_at', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address')
    inlines = [ServiceOrderFieldValueInline]

    def has_add_permission(self, request):
        return request.user.groups.filter(name='Developpers').exists()  # Seuls les utilisateurs du groupe "Developpers" peuvent ajouter des commandes

    def get_fields(self, request, obj=None):
        if obj and request.user.groups.filter(name='Developpers').exists():
            return ('service', 'quantity', 'width', 'height', 'image', 'img_path', 'comment', 'delivery_mode','client_name', 'client_email', 'client_phone', 'client_address')
        return ('service', 'quantity', 'width', 'height', 'image', 'comment', 'delivery_mode','client_name', 'client_email', 'client_phone', 'client_address')


class GalerieImageForServiceInline(admin.TabularInline):
    model = GalerieImageForService
    extra = 0

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [GalerieImageForServiceInline, ServiceFieldInline]
    list_display = ('name',)
    #fields = ('name', 'description', 'description_accueil',)

    class Media:
        js = ('Services/js/admin/services.js',)  
    
    # SOLUTION : Utilisation dynamique de fieldsets pour inclure vos consignes en haut du formulaire
    def get_fieldsets(self, request, obj=None):
        # 1. On définit la liste des champs de base selon le rôle (votre logique get_fields initiale)
        base_fields = ['name', 'description', 'description_accueil']
        if obj and request.user.groups.filter(name='Developpers').exists():
            base_fields.append('slug')
            
        # 2. On retourne la structure finale avec les consignes intégrées proprement
        return (
            ("Consignes importantes pour les champs spécifiques", {
                'description': (
                    "⚠️ Consignes d'utilisation : Ce formulaire permet de configurer "
                    "les champs spécifiques aux services. Veillez à respecter la nomenclature. "
                    "Ce modèle définit les champs spécifiques à chaque service, permettant une "
                    "personnalisation dynamique des formulaires de commande. Les champs comme Longueur, "
                    "Largeur, Quantité, Commentaire (Instructions Spéciales) sont communs à tous les "
                    "services et ne doivent pas être ajoutés."
                ),
                'fields': base_fields,
            }),
        )
