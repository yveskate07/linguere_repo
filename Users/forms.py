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



