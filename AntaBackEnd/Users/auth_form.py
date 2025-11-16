from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Fab_User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True , widget=forms.TextInput(attrs={'name':'username','id':'username','placeholder': "Entrer le nom d'utilisateur", "autofocus": True}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'name':'password','id':'password','placeholder': "Entrez votre mot de passe", "autocomplete": "current-password"}))

class UserSignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirmation du mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'id': 'confirm_password',
            'placeholder': 'Confirmez le mot de passe'
        })
    )

    class Meta:
        model = Fab_User
        fields = ['last_name', 'first_name', 'email','username', 'password','tel_num', 'adress']
        widgets = {
            'last_name': forms.TextInput(attrs={
                'id': 'lastname',
                'required': True,
                'placeholder': 'Votre nom'
            }),
            'first_name': forms.TextInput(attrs={
                'id': 'firstname',
                'required': True,
                'placeholder': 'Vos prénoms'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'required': True,
                'placeholder': 'exemple@email.com'
            }),
            'username': forms.TextInput(attrs={
                'id': 'username',
                'required': True,
                'placeholder': "Choisissez un nom d'utilisateur"
            }),
            'password' : forms.PasswordInput(attrs={
                'id': 'password',
                'required': True,
                'placeholder': 'Choisissez un mot de passe'
            }),
            'tel_num': forms.TextInput(attrs={  # ou forms.TelInput si souhaité
                'id': 'phone',
                'required': True,
                'placeholder': 'Votre numéro',
                'type': 'tel'
            }),
            'adress': forms.TextInput(attrs={
                'id': 'address',
                'required': True,
                'placeholder': 'Votre adresse complète'
            }),
        }

    def clean(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if Fab_User.objects.filter(username=username).exists():
            raise forms.ValidationError("Cet nom d'utilisateur est déjà utilisé.")

        return username