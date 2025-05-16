from django.contrib import admin

from Services.models import Service


# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('name','description','image1','image2','image3','image4','image5','image6','image7','image8',)
    list_display = ('name','description',)