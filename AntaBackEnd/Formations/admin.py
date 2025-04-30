from django.contrib import admin
from django.contrib.auth.models import Group

from Formations.models import *


admin.site.unregister(Group)

# Register your models here.
@admin.register(Formations)
class FormationAdmin(admin.ModelAdmin):
    fields = ('name','motiv','duration', 'description','image','determinant','availability','hours_per_week',)
    readonly_fields = ('description',)
    list_display = ('name','get_duration_display_fr','hours_per_week','availability',)

    def get_duration_display_fr(self, obj):
        return obj.get_duration_display_fr()

    get_duration_display_fr.short_description = 'Durée'



    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name','formation', 'description',)
    list_display = ('name', 'formation',)
    readonly_fields = ('description',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Prerequisites)
class PrerequisitesAdmin(admin.ModelAdmin):
    fields = ('name','level','image','formation',)
    list_display = ('name', 'level','formation',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SkillGained)
class SkillGainedAdmin(admin.ModelAdmin):
    fields = ('name','description_skill','formation',)
    list_display = ('name','description_skill','formation',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(MotivPoints)
class MotivPointsAdmin(admin.ModelAdmin):
    fields = ('name','description','formation',)
    list_display = ('name', 'description','formation',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Advantages)
class AdvantagesAdmin(admin.ModelAdmin):
    fields = ('name', 'description','formation',)
    list_display = ('name', 'description','formation',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    fields = ('formation','username','status','comment', 'description',)
    list_display = ('formation','username','status','comment',)
    readonly_fields = ('description',)

    """def has_add_permission(self, request):
        return False"""

@admin.register(SignedUpUser)
class SignedUpUserAdmin(admin.ModelAdmin):
    fields = ('name','email','tel_number','formation_method','session','formation', 'description',)
    readonly_fields = ('description',)

    list_display = ('name','email','tel_number','formation_method','session','formation')

    """def has_add_permission(self, request):
        return False"""

@admin.register(UserBrochure)
class UserBrochureAdmin(admin.ModelAdmin):
    fields = ('name','email','method','formation', 'description',)
    list_display = ('name','email','method','formation',)
    readonly_fields = ('description',)

    """def has_add_permission(self, request):
        return False"""

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    fields = ('name','email','formation', 'description',)
    list_display = ('name', 'email', 'formation',)
    readonly_fields = ('description',)

    """def has_add_permission(self, request):
        return False"""