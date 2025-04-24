from django.contrib import admin
from Formations.models import *


# Register your models here.
@admin.register(Formations)
class FormationAdmin(admin.ModelAdmin):
    fields = ('name','motiv','price','availability',)

admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name',)

@admin.register(Prerequisites)
class PrerequisitesAdmin(admin.ModelAdmin):
    fields = ('name','level',)

@admin.register(SkillGained)
class SkillGainedAdmin(admin.ModelAdmin):
    fields = ('name','description',)

