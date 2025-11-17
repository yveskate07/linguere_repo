from django.contrib import admin
from .models import *

class ActivityGalerieImageInline(admin.TabularInline):
    model = ActivityGalerieImage

class RealisationInline(admin.TabularInline):
    model = Realisation

class ResultatInline(admin.TabularInline):
    model = Resultat

class ImpactInline(admin.TabularInline):
    model = Impact


# Register your models here.
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    inlines = [ActivityGalerieImageInline, RealisationInline, ResultatInline, ImpactInline]
    list_display = ('name', 'created_at')

