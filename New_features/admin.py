from django.contrib import admin

from .models import Feature

# Register your models here.
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ("description", "image", )