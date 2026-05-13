from django.contrib import admin

from .models import *


class GalerieImageForServiceInline(admin.TabularInline):
    model = GalerieImageForService
    extra = 0

class ColorInline(admin.TabularInline):
    model = Colors
    extra = 0

@admin.register(BroderieNumeriqueModel)
class BroderieNumeriqueModelAdmin(admin.ModelAdmin):
    inlines = [ColorInline]
    list_display = ('support_type', 'other_support', 'created_at', 'quantity', 'width','height', 'client_name', 'client_email','client_phone','client_address','delivery_mode',)
    fieldsets = (
        ("Cuztomization Infos", {
            'fields': ('support_type', 'other_support', 'comment', 'quantity', 'width','height', 'image')
        }),
        ('Client Infos', {
            'fields': ('client_name', 'client_email','client_phone','client_address','delivery_mode')
        }),
    )

@admin.register(FraiseCNCModel)
class FraiseCNCModelAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'used_material', 'created_at', 'quantity', 'width', 'height', 'client_name', 'client_email','client_phone','client_address','delivery_mode',)
    
    fieldsets = (
        ("Cuztomization Infos", {
            'fields': ('service_type', 'used_material', 'comment', 'quantity', 'width','height', 'image')
        }),
        ('Client Infos', {
            'fields': ('client_name', 'client_email','client_phone','client_address','delivery_mode')
        }),
    )

@admin.register(DecoupeLaserModel)
class DecoupeLaserModelAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'used_material', 'created_at', 'quantity', 'width', 'height', 'client_name', 'client_email','client_phone','client_address','delivery_mode',)
    
    fieldsets = (
        ("Cuztomization Infos", {
            'fields': ('service_type', 'used_material', 'comment', 'quantity', 'width','height', 'image')
        }),
        ('Client Infos', {
            'fields': ('client_name', 'client_email','client_phone','client_address','delivery_mode')
        }),
    )

@admin.register(Impression3DModel)
class Impression3DModelAdmin(admin.ModelAdmin):
    list_display = ('impression_type', 'used_material', 'created_at', 'quantity', 'width', 'height', 'client_name', 'client_email','client_phone','client_address','delivery_mode',)
    inlines = [ColorInline]

    fieldsets = (
        ("Cuztomization Infos", {
            'fields': ('impression_type', 'used_material', 'comment', 'quantity', 'width','height', 'image')
        }),
        ('Client Infos', {
            'fields': ('client_name', 'client_email','client_phone','client_address','delivery_mode')
        }),
    )

@admin.register(ImpressionPaperSupportRigideModel)
class ImpressionPaperSupportRigideModelAdmin(admin.ModelAdmin):
    list_display = ('format', 'other_format', 'paper_type', 'other_paper', 'design_file', 'other_file', 'created_at', 'quantity', 'width', 'height', 'client_name', 'client_email','client_phone','client_address','delivery_mode',)
    inlines = [ColorInline]

    fieldsets = (
        ("Cuztomization Infos", {
            'fields': ('format', 'other_format', 'paper_type', 'other_paper', 'design_file', 'other_file', 'comment', 'quantity', 'width','height', 'image')
        }),
        ('Client Infos', {
            'fields': ('client_name', 'client_email','client_phone','client_address','delivery_mode')
        }),
    )

@admin.register(ImpressionTextileEtVetementModel)
class ImpressionTextileEtVetementModelAdmin(admin.ModelAdmin):
    list_display = ('textile_type', 'other_textile', 'impression_type', 'design_file', 'other_design_file', 'created_at', 'quantity', 'width', 'height', 'client_email','client_phone','client_address','delivery_mode',)
    inlines = [ColorInline]

    fieldsets = (
        ("Cuztomization Infos", {
            'fields': ('textile_type', 'other_textile', 'impression_type', 'design_file', 'other_design_file', 'comment', 'quantity', 'width','height', 'image')
            }),
        ('Client Infos', {
            'fields': ('client_name', 'client_email','client_phone','client_address','delivery_mode')
        }),
    )

@admin.register(ImpressionObjPersonnaliseModel)
class ImpressionObjPersonnaliseModelAdmin(admin.ModelAdmin):
    inlines = [ColorInline]
    list_display = ('obj_type', 'other_object', 'design_file', 'other_file' , 'created_at', 'quantity', 'width', 'height', 'client_email','client_phone','client_address','delivery_mode')

    fieldsets = (
        ("Cuztomization Infos", {
            'fields': ('obj_type', 'other_object', 'design_file', 'other_file', 'comment', 'quantity', 'width','height', 'image')
        }),
        ("Client Infos", {'fields': ('client_name', 'client_email','client_phone','client_address','delivery_mode')})
    ) 

# Register your models here.
@admin.register(ServiceInfo)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'description_accueil','slug',)
    inlines = [GalerieImageForServiceInline]
    list_display = ('name',)

    def get_fields(self, request, obj=None):
        if obj:  # édition
            if request.user.groups.filter(name="Developpers").exists():
                return ('name', 'description', 'description_accueil','slug', 'impressionNumerique','class_icon_name',)
            return ('name', 'description', 'description_accueil','slug',)
        else:    # création
            return ('name', 'description', 'description_accueil','slug',)

    def get_readonly_fields(self, request, obj = ...):
        readonly = list(super().get_readonly_fields(request, obj))

        if request.user.has_perm('Services.edit_Services_service_name'):
            try:
                readonly.remove('name')
            except ValueError:
                pass
        else:
            if not 'name' in readonly:
                readonly.append('name')

        if not request.user.has_perm('Services.edit_Services_services_slug'):
            if not 'slug' in readonly:
                readonly.append('slug')
        else:
            try:
                readonly.remove('slug')
            except ValueError:
                pass


        if not request.user.has_perm('Services.change_service_imp_bool'):
            if not 'impressionNumerique' in readonly:
                readonly.append('impressionNumerique')
        else:
            try:
                readonly.remove('impressionNumerique')
            except ValueError:
                pass


        return readonly
    
    def has_delete_permission(self, request, obj = ...):
        return super().has_delete_permission(request, obj) and request.user.has_perm('Services.delete_Service')
    
    def has_add_permission(self, request):
        return super().has_add_permission(request) and request.user.has_perm('Services.add_service')
    
    def has_add_permission(self, request):
        if ServiceInfo.objects.count() >= 7:
            return False
        return super().has_add_permission(request)