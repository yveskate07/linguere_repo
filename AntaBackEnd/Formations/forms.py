from django import forms
from .models import SignedUpUser, UserBrochure, UserRequest



class SignedUpUserForm(forms.ModelForm):
    class Meta:
        model = SignedUpUser
        fields = ['availability', 'session', 'message']

        widgets = {
            'availability': forms.Select(attrs={
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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     email = cleaned_data.get('email')
    #
    #     if name:
    #         cleaned_data['name'] = name.strip()
    #     if email:
    #         cleaned_data['email'] = email.strip()
    #
    #     if cleaned_data.get('name') and cleaned_data.get('email'):
    #         if SignedUpUser.objects.filter(
    #             name__iexact=cleaned_data['name'],
    #             email__iexact=cleaned_data['email']
    #         ).exists():
    #             print("Un utilisateur avec ce nom et cet email est déjà inscrit.")
    #             raise forms.ValidationError(
    #                 "Un utilisateur avec ce nom et cet email est déjà inscrit."
    #             )
    #
    #         else:
    #             print("Enregistrement d'un nouveau client")
    #
    #     return cleaned_data


class BrochureForm(forms.ModelForm):
    class Meta:
        model = UserBrochure
        fields = ['availability', 'message']

        widgets = {
            'availability': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'id': "method"}),

            'message': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'id': "message", 'rows': 3,
                'placeholder': 'Avez-vous des questions ou des besoins spécifiques ?'})
        }


class RequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ['message']

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 mt-1 focus:ring-indigo-500 focus:border-indigo-500',
                'id': "contact-message", 'rows': 3,
                'placeholder': 'Avez-vous des questions ou des besoins spécifiques ?'})
        }