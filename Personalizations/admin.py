from django.contrib import admin
from .models import ImagesOnHomepage


# Register your models here.
@admin.register(ImagesOnHomepage)
class ImagesOnHomepageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id',)
    fields = ('image1', 'image2', 'image3')
    