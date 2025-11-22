from django import forms
from .models import Fab_User


class UserEditForm(forms.ModelForm):
    tel_num = forms.CharField(
        label="Numéro de téléphone",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Ex: +221771234567"})
    )
    adress = forms.CharField(
        label="Adresse",
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Ex: Dakar, Sénégal"})
    )
    picture_profile = forms.ImageField(label="Photo de profil")

    class Meta:
        model = Fab_User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "tel_num",
            "adress",
            "picture_profile"
        ]

        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Nom de famille"}),
            "email": forms.EmailInput(attrs={"placeholder": "Adresse e-mail"}),
            "tel_num": forms.TextInput(attrs={"placeholder": "Ex: +221771234567"}),
            "adress": forms.Textarea(attrs={"rows": 3, "placeholder": "Ex: Dakar, Sénégal"}),
            "picture_profile": forms.ClearableFileInput(),
        }
        labels = {
            "tel_num": "Numéro de téléphone",
            "adress": "Adresse",
            "picture_profile": "Photo de profil",
        }


class UserResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Entrez le nouveau mot de passe"})
    )
    new_password2 = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmez le nouveau mot de passe"})
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data