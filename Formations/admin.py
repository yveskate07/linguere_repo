from re import S
from django.contrib import admin
from Formations.models import *

class ModuleInline(admin.TabularInline):
    model = Module

class PrerequisitesInline(admin.TabularInline):
    model = Prerequisites

class SkillGainedInline(admin.TabularInline):
    model = SkillGained

'''class MotivPointsInline(admin.TabularInline):
    model = MotivPoints'''

class AdvantagesInline(admin.TabularInline):
    model = Advantages

class AskedQuestionsInline(admin.TabularInline):
    model = AskedQuestions

"""
class TestimonyInline(admin.TabularInline):
    model = Testimony"""

@admin.register(SignedUpUser)
class SignedUpAdmin(admin.ModelAdmin):
    list_display = ('user','availability','session','formation',)
    fields = ('user','availability','session','formation', 'message',)

@admin.register(UserBrochure)
class UserBrochureAdmin(admin.ModelAdmin):
    list_display = ('user','availability','formation',)
    fields = ('user','availability','formation', 'message',)

    def has_view_permission(self, request, obj = ...):

        if request.user.is_staff and not request.user.is_superuser:
            True
        else:
            return False

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'formation',)
    fields = ('user', 'message', 'formation')

    def has_view_permission(self, request, obj = ...):

        if request.user.is_staff and not request.user.is_superuser:
            True
        else:
            return False

# Register your models here.
@admin.register(Formations)
class FormationAdmin(admin.ModelAdmin):
    inlines = [ModuleInline, PrerequisitesInline, SkillGainedInline, AdvantagesInline, AskedQuestionsInline]
    fields = ('name','duration', 'price', 'image','availability','hours_per_week','image_home','why_image',)
    list_display = ('name','get_duration_display_fr','hours_per_week','availability', 'price')
    search_fields = ('name',)
    list_filter = ('availability',)

    def get_duration_display_fr(self, obj):
        return obj.get_duration_display_fr()
    
    def get_fields(self, request, obj=None): # Utilisez None par défaut, pas ...
        # Si c'est un superutilisateur et qu'on modifie un objet existant
        if obj and request.user.groups.filter(name='Developpers').exists():
            return ('name','duration', 'price','image','availability','hours_per_week','image_home','why_image','slug','css_cls_parent_in_home','css_ps_cls_in_home', 'data_aos', 'data_aos_duration')
        
        # Retourne les champs par défaut définis plus haut ou par le parent
        return super().get_fields(request, obj)
    
    def get_readonly_fields(self, request, obj = ...):
        readonly = list(super().get_readonly_fields(request, obj))

        if not request.user.has_perm('Formations.edit_Formations_formation_name'):
            readonly.append('name')

        if not request.user.has_perm('Formations.edit_Formations_formation_slug'):
            readonly.append('slug')

        return readonly

    get_duration_display_fr.short_description = 'Durée'


'''
@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    fields = ('formation','username','status','comment', 'description',)
    list_display = ('formation','status','comment',)
    readonly_fields = ('description',)

    """def has_add_permission(self, request):
        return False"""

@admin.register(SignedUpUser)
class SignedUpUserAdmin(admin.ModelAdmin):
    fields = ('availability','session','formation', 'description',)
    list_filter = ('formation','session','availability',)
    #search_fields = ('name',)
    readonly_fields = ('description',)

    #list_display = ('name','email','tel_number','availability','session','formation')
    list_display = ('availability', 'session', 'formation')

    """def has_add_permission(self, request):
        return False"""

@admin.register(UserBrochure)
class UserBrochureAdmin(admin.ModelAdmin):
    fields = ('availability','formation', 'description',)
    list_display = ('availability','formation',)
    #search_fields = ('name',)
    list_filter = ('availability','formation',)
    readonly_fields = ('description',)

    """def has_add_permission(self, request):
        return False"""

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    fields = ('formation', 'description',)
    list_display = ('formation',)
    #search_fields = ('name',)
    list_filter = ('formation',)
    readonly_fields = ('description',)

    """def has_add_permission(self, request):
        return False"""'''