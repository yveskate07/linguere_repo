from re import S
from django.contrib import admin
from django.contrib.auth.models import Group

from Formations.models import *


admin.site.unregister(Group)

class ModuleInline(admin.TabularInline):
    model = Module

class PrerequisitesInline(admin.TabularInline):
    model = Prerequisites

class SkillGainedInline(admin.TabularInline):
    model = SkillGained

class MotivPointsInline(admin.TabularInline):
    model = MotivPoints

class AdvantagesInline(admin.TabularInline):
    model = Advantages
"""
class TestimonyInline(admin.TabularInline):
    model = Testimony"""

@admin.register(SignedUpUser)
class SignedUpAdmin(admin.ModelAdmin):
    list_display = ('user','availability','session','formation',)
    fields = ('user','availability','session','formation', 'message',)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(UserBrochure)
class UserBrochureAdmin(admin.ModelAdmin):
    list_display = ('user','availability','formation',)
    fields = ('user','availability','formation', 'message',)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'formation',)
    fields = ('user', 'message', 'formation')

    def has_delete_permission(self, request, obj=None):
        return False

# Register your models here.
@admin.register(Formations)
class FormationAdmin(admin.ModelAdmin):
    inlines = [ModuleInline, PrerequisitesInline, SkillGainedInline, MotivPointsInline, AdvantagesInline]
    fields = ('name','duration','image','availability','hours_per_week','image_home','why_image',)
    #readonly_fields = ('description',)
    list_display = ('name','get_duration_display_fr','hours_per_week','availability',)
    search_fields = ('name',)
    list_filter = ('availability',)

    def get_duration_display_fr(self, obj):
        return obj.get_duration_display_fr()

    get_duration_display_fr.short_description = 'Durée'



    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


'''@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('name','formation', 'description',)
    search_fields = ('name',)
    list_filter = ('formation',)
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
    search_fields = ('name',)
    list_filter = ('level','formation',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SkillGained)
class SkillGainedAdmin(admin.ModelAdmin):
    fields = ('name','description_skill','formation',)
    list_filter = ('formation',)
    list_display = ('name','description_skill','formation',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(MotivPoints)
class MotivPointsAdmin(admin.ModelAdmin):
    fields = ('name','description','formation',)
    list_filter = ('formation',)
    list_display = ('name', 'description','formation',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Advantages)
class AdvantagesAdmin(admin.ModelAdmin):
    fields = ('name', 'description','formation',)
    list_filter = ('formation',)
    list_display = ('name', 'description','formation',)

    """def has_add_permission(self, request):
        return False"""

    def has_delete_permission(self, request, obj=None):
        return False

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