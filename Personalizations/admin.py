from django.contrib import admin
from .models import ImagesOnHomepage


# Register your models here.
@admin.register(ImagesOnHomepage)
class ImagesOnHomepageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id',)
    fields = ('image1', 'image2', 'image3')

    def has_add_permission(self, request):
        if ImagesOnHomepage.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    