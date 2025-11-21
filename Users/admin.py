from django.contrib import admin
from Users.models import Fab_User


# Register your models here.

@admin.register(Fab_User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email",)

    def has_delete_permission(self, request, obj=None):
        return True