from django import forms

from Services.models import CustomizedService


class CustomizedServiceForm(forms.ModelForm):
    """
    formulaire utilisé lorsque l'utilisateur customise un service
    """

    class Meta:
        model = CustomizedService
        fields = ['imported_picture', 'chosen_picture', 'adress_delivery', 'delivery_mode', 'cgu_accept']
        widgets = {'imported_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'adress_delivery': forms.TextInput(attrs={'class':'form-control','id':'address'}), 
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms','class':'form-check-input'}),
                   }
