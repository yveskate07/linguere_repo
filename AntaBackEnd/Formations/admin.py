from django.contrib import admin
from django.contrib.auth.models import Group

from Formations.models import *


admin.site.unregister(Group)

# Register your models here.
@admin.register(Formations)
class FormationAdmin(admin.ModelAdmin):
    fields = ('name','motiv','duration','slug',)


admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name',)

@admin.register(Prerequisites)
class PrerequisitesAdmin(admin.ModelAdmin):
    fields = ('name','level',)

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    fields = ('formation','username','status','comment')

@admin.register(SignedUpUser)
class SignedUpUserAdmin(admin.ModelAdmin):
    fields = ('name','email','tel_number','formation_method','session','formation')

    list_display = ('name','email','tel_number','formation_method','session','formation')

@admin.register(UserBrochure)
class UserBrochureAdmin(admin.ModelAdmin):
    fields = ('name','email','method','formation',)

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    fields = ('name','email','formation',)