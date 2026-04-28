from django.contrib import admin
from Testimonies.models import Testimony

# Register your models here.
@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'testimony', 'picture', 'user_short_description')
        }),
    )   
    list_display = ('name', 'user_short_description', 'created_at',)
    def has_add_permission(self, request):
        if Testimony.objects.count() >= 3:
            return False
        return super().has_add_permission(request)