from django.contrib import admin
from .models import *

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
    fields = ('name', 'description', 'description_accueil', 'presentation_img', 'motiv1', 'motiv2',)
    
    def get_fields(self, request, obj=None):
        if obj and request.user.groups.filter(name='Developpers').exists():
            return ('name', 'description', 'description_accueil', 'presentation_img', 'motiv1', 'motiv2','url_name',)
        
        if not request.user.has_perm('Activities.edit_Activities_activity_name'):
            return ('description', 'description_accueil', 'presentation_img', 'motiv1', 'motiv2','url_name',)
        
        return super().get_fields(request, obj)