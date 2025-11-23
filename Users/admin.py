from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect
from .models import Fab_User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Fab_User
        fields = ("username", "email", "first_name", "last_name", "tel_num", "adress")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Fab_User
        fields = "__all__"


@admin.register(Fab_User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "email", "tel_num", "adress")}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )
    """fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "email", "tel_num", "adress")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )"""
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "tel_num", "adress", "password1", "password2"),
        }),
    )

    def response_add(self, request, obj, post_url_continue=None):
        """
        Après ajout, on revient toujours à la liste des utilisateurs.
        """
        return HttpResponseRedirect("../")