from django.contrib import admin
from django.contrib.auth.models import Group

from Formations.models import *


admin.site.unregister(Group)

# Register your models here.
@admin.register(Formations)
class FormationAdmin(admin.ModelAdmin):
    fields = ('name','motiv','duration', 'description',)
    readonly_fields = ('description',)
    list_display = ('name','duration',)

    def has_add_permission(self, request):
        return False



@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name','formation', 'description',)
    list_display = ('name', 'formation',)
    readonly_fields = ('description',)

    def has_add_permission(self, request):
        return False

"""@admin.register(Prerequisites)
class PrerequisitesAdmin(admin.ModelAdmin):
    fields = ('name','level',)"""

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    fields = ('formation','username','status','comment', 'description',)
    list_display = ('formation','username','status','comment',)
    readonly_fields = ('description',)

    def has_add_permission(self, request):
        return False

@admin.register(SignedUpUser)
class SignedUpUserAdmin(admin.ModelAdmin):
    fields = ('name','email','tel_number','formation_method','session','formation', 'description',)
    readonly_fields = ('description',)

    list_display = ('name','email','tel_number','formation_method','session','formation')

    def has_add_permission(self, request):
        return False

@admin.register(UserBrochure)
class UserBrochureAdmin(admin.ModelAdmin):
    fields = ('name','email','method','formation', 'description',)
    list_display = ('name','email','method','formation',)
    readonly_fields = ('description',)

    def has_add_permission(self, request):
        return False

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    fields = ('name','email','formation', 'description',)
    list_display = ('name', 'email', 'formation',)
    readonly_fields = ('description',)

    def has_add_permission(self, request):
        return False