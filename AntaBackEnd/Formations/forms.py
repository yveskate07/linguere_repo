from django import forms
from .models import SignedUpUser, UserBrochure, UserRequest


class SignedUpUserForm(forms.ModelForm):
    class Meta:
        model = SignedUpUser
        fields = ['name', 'email', 'tel_number', 'formation_method', 'session', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Entrez votre nom complet', 'id': 'inscription-name', 'name': 'inscription-name'}),

            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500'
                , 'placeholder': 'Entrez votre adresse e-mail', 'id': 'inscription-email',
        }),

            'tel_number': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Entrez votre numéro de téléphone', 'id': "inscription-phone",
        }),

            'formation_method': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'id': "inscription-method"}),

            'session': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'id': "inscription-session"}),

            'message': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'id': "inscription-message", 'rows': 3,
                'placeholder': 'Avez-vous des questions ou des besoins spécifiques ?'}),
        }


class BrochureForm(forms.ModelForm):
    class Meta:
        model = UserBrochure
        fields = ['name', 'email', 'tel_number', 'method']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Entrez votre nom complet', 'id': 'name', 'name': 'name'}),

            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500'
                , 'placeholder': 'Entrez votre adresse e-mail', 'id': 'email'}),

            'tel_number': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Entrez votre numéro de téléphone', 'id': "phone"}),

            'method': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'id': "method"})}


class RequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ['name', 'email', 'tel_number', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Entrez votre nom complet', 'id': 'contact-name'}),

            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500'
                , 'placeholder': 'Entrez votre adresse e-mail', 'id': 'contact-email'}),

            'tel_number': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Entrez votre numéro de téléphone', 'id': "contact-phone"}),

            'message': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'id': "contact-message", 'rows': 3,
                'placeholder': 'Avez-vous des questions ou des besoins spécifiques ?'})
        }