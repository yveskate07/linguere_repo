from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect
from .models import Fab_User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Fab_User
        fields = ("username", "email", "first_name", "last_name", "tel_num", "adress", "is_active", "is_staff", )


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
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_admin",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "tel_num",
                    "adress",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    FORBIDDEN_FIELDS = {"is_admin", "groups", "user_permissions"}
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if request.user.groups.filter(name="Developpers").exists():
            return fieldsets

        filtered = []
        for name, data in fieldsets:
            fields = data.get("fields", ())
            new_fields = [f for f in fields if f not in self.FORBIDDEN_FIELDS]
            filtered.append((name, {**data, "fields": new_fields}))

        return filtered

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))

        if not request.user.has_perm('Activities.edit_Activities_activity_name'):
            
            readonly.append('name')

        if not request.user.has_perm('Activities.edit_Activities_activity_url_name'):
            
            readonly.append('url_name')

        return readonly
    
    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_admin:
            return True
        
        return super().has_add_permission(request)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_admin:
            return True
        
        
        return super().has_change_permission(request, obj)

    """def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            # rendre certains champs non modifiables
            disabled_fields = {"is_superuser", "groups", "user_permissions"}

            for field in disabled_fields:
                if field in form.base_fields:
                    form.base_fields[field].disabled = True

        return form"""

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(f"{obj.id}/change/")
    
    def save_model(self, request, obj, form, change):
        # Si l'utilisateur qu'on sauvegarde n'est pas superuser
        if not obj.is_superuser:
            try:
                perm = Permission.objects.get(codename="view_group", content_type__app_label="auth", content_type__model="group")
                obj.user_permissions.remove(perm)

            except (ValueError, Permission.DoesNotExist):
                pass

        super().save_model(request, obj, form, change)
