from django import forms

from Services.models import *


class AnonymousBroderieNumeriqueModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service de broderie numérique, pour les utilisateurs non authentifiés, donc les champs client sont demandés
    """

    class Meta:
        model = BroderieNumeriqueModel
        fields = ['image', 'support_type', 'other_support', 'comment', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'support_type': forms.Select(attrs={'class':'option-select','id':'support-type'}),
                   'other_support': forms.TextInput(attrs={'class':'option-input','id':'other-support','placeholder':'Précisez le type de support', 'style':'display: none; margin-top: 0.8rem;'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '50'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '50'}),
                   'client_name': forms.TextInput(attrs={'class':'form-control','id':'client-name'}),
                   'client_email': forms.EmailInput(attrs={'class':'form-control','id':'client-email'}),
                   'client_phone': forms.TextInput(attrs={'class':'form-control','id':'client-phone'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }
        
class BroderieNumeriqueModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service de broderie numérique, 
    pour les utilisateurs authentifiés, 
    donc les champs client ne sont pas demandés car ils sont pris depuis le compte utilisateur
    """

    class Meta:
        model = BroderieNumeriqueModel
        fields = ['image', 'support_type', 'other_support', 'comment', 'quantity', 'width', 'height', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'support_type': forms.Select(attrs={'class':'option-select','id':'support-type'}),
                   'other_support': forms.TextInput(attrs={'class':'option-input','id':'other-support','placeholder':'Précisez le type de support', 'style':'display: none; margin-top: 0.8rem;'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '50'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '50'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }

class DecoupeLaserModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service de découpe et gravure laser, 
    pour les utilisateurs authentifiés, 
    donc les champs client ne sont pas demandés car ils sont pris depuis le compte utilisateur
    """

    class Meta:
        model = DecoupeLaserModel
        fields = ['image', 'service_type', 'used_material', 'comment', 'quantity', 'width', 'height', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'service_type': forms.Select(attrs={'class':'option-select','id':'service-type'}),
                   'used_material': forms.Select(attrs={'class':'option-select','id':'used-material'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }
        
class AnonymousDecoupeLaserModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service de découpe et gravure laser, 
    pour les utilisateurs non authentifiés, donc les champs client sont demandés
    """

    class Meta:
        model = DecoupeLaserModel
        fields = ['image', 'service_type', 'used_material', 'comment', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'service_type': forms.Select(attrs={'class':'option-select','id':'service-type'}),
                   'used_material': forms.Select(attrs={'class':'option-select','id':'used-material'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_name': forms.TextInput(attrs={'class':'form-control','id':'client-name'}),
                   'client_email': forms.EmailInput(attrs={'class':'form-control','id':'client-email'}),
                   'client_phone': forms.TextInput(attrs={'class':'form-control','id':'client-phone'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }
        
class FraiseCNCModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service de fraiseuse numérique CNC, 
    pour les utilisateurs authentifiés, 
    donc les champs client ne sont pas demandés car ils sont pris depuis le compte utilisateur
    """

    class Meta:
        model = FraiseCNCModel
        fields = ['image', 'service_type', 'used_material', 'comment', 'quantity', 'width', 'height', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'service_type': forms.Select(attrs={'class':'option-select','id':'service-type'}),
                   'used_material': forms.Select(attrs={'class':'option-select','id':'used-material'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }

class AnonymousFraiseCNCModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service de fraiseuse numérique CNC, 
    pour les utilisateurs non authentifiés, donc les champs client sont demandés
    """

    class Meta:
        model = FraiseCNCModel
        fields = ['image', 'service_type', 'used_material', 'comment', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'service_type': forms.Select(attrs={'class':'option-select','id':'service-type'}),
                   'used_material': forms.Select(attrs={'class':'option-select','id':'used-material'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_name': forms.TextInput(attrs={'class':'form-control','id':'client-name'}),
                   'client_email': forms.EmailInput(attrs={'class':'form-control','id':'client-email'}),
                   'client_phone': forms.TextInput(attrs={'class':'form-control','id':'client-phone'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }

class Impression3DModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service d'impression 3D, 
    pour les utilisateurs authentifiés, 
    donc les champs client ne sont pas demandés car ils sont pris depuis le compte utilisateur
    """

    class Meta:
        model = Impression3DModel
        fields = ['image', 'impression_type', 'used_material', 'comment', 'quantity', 'width', 'height', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'impression_type': forms.Select(attrs={'class':'option-select','id':'impression-type'}),
                   'used_material': forms.Select(attrs={'class':'option-select','id':'used-material'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }
        
class AnonymousImpression3DModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service d'impression 3D, 
    pour les utilisateurs non authentifiés, donc les champs client sont demandés
    """

    class Meta:
        model = Impression3DModel
        fields = ['image', 'impression_type', 'used_material', 'comment', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'impression_type': forms.Select(attrs={'class':'option-select','id':'impression-type'}),
                   'used_material': forms.Select(attrs={'class':'option-select','id':'used-material'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_name': forms.TextInput(attrs={'class':'form-control','id':'client-name'}),
                   'client_email': forms.EmailInput(attrs={'class':'form-control','id':'client-email'}),
                   'client_phone': forms.TextInput(attrs={'class':'form-control','id':'client-phone'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }

class ImpressionObjPersonnaliseModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service d'impression sur objets personnalisés, 
    pour les utilisateurs authentifiés, 
    donc les champs client ne sont pas demandés car ils sont pris depuis le compte utilisateur
    """

    class Meta:
        model = ImpressionObjPersonnaliseModel
        fields = ['image', 'obj_type', 'other_object', 'design_file', 'other_file', 'comment', 'quantity', 'width', 'height', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'obj_type': forms.Select(attrs={'class':'option-select','id':'object-type'}),
                   'other_object': forms.TextInput(attrs={'class':'option-input','id':'other-object','placeholder':"Précisez l'objet", 'style':'display: none; margin-top: 0.8rem;'}),
                   'design_file': forms.Select(attrs={'class':'option-select','id':'design-file'}),
                   'other_file': forms.TextInput(attrs={'class':'option-input','id':'other-file','placeholder':'Précisez un autre fichier si nécessaire', 'style':'display: none; margin-top: 0.8rem;'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }

class AnonymousImpressionObjPersonnaliseModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service d'impression sur objets personnalisés, 
    pour les utilisateurs non authentifiés, donc les champs client sont demandés
    """

    class Meta:
        model = ImpressionObjPersonnaliseModel
        fields = ['image', 'obj_type', 'other_object', 'design_file', 'other_file', 'comment', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'obj_type': forms.Select(attrs={'class':'option-select','id':'object-type'}),
                   'other_object': forms.TextInput(attrs={'class':'option-input','id':'other-object','placeholder':"Précisez l'objet", 'style':'display: none; margin-top: 0.8rem;'}),
                   'design_file': forms.Select(attrs={'class':'option-select','id':'design-file'}),
                   'other_file': forms.TextInput(attrs={'class':'option-input','id':'other-file','placeholder':'Précisez un autre fichier si nécessaire', 'style':'display: none; margin-top: 0.8rem;'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_name': forms.TextInput(attrs={'class':'form-control','id':'client-name'}),
                   'client_email': forms.EmailInput(attrs={'class':'form-control','id':'client-email'}),
                   'client_phone': forms.TextInput(attrs={'class':'form-control','id':'client-phone'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }
        
class ImpressionPaperSupportRigideModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service d'impression sur papier et supports rigides, 
    pour les utilisateurs authentifiés, 
    donc les champs client ne sont pas demandés car ils sont pris depuis le compte utilisateur
    """

    class Meta:
        model = ImpressionPaperSupportRigideModel
        fields = ['image', 'format', 'other_format', 'paper_type', 'other_paper', 'design_file', 'other_file', 'comment', 'quantity', 'width', 'height', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'format': forms.Select(attrs={'class':'option-select','id':'format'}),
                   'other_format': forms.TextInput(attrs={'class':'option-input','id':'other-format','placeholder':'Précisez le format', 'style':'display: none; margin-top: 0.8rem;'}),
                   'paper_type': forms.Select(attrs={'class':'option-select','id':'paper-type'}),
                   'other_paper': forms.TextInput(attrs={'class':'option-input','id':'other-paper','placeholder':'Précisez le type de papier', 'style':'display: none; margin-top: 0.8rem;'}),
                   'design_file': forms.Select(attrs={'class':'option-select','id':'design-file'}),
                   'other_file': forms.TextInput(attrs={'class':'option-input','id':'other-file','placeholder':'Précisez un autre fichier si nécessaire', 'style':'display: none; margin-top: 0.8rem;'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }

class AnonymousImpressionPaperSupportRigideModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service d'impression sur papier et supports rigides, 
    pour les utilisateurs non authentifiés, donc les champs client sont demandés
    """

    class Meta:
        model = ImpressionPaperSupportRigideModel
        fields = ['image', 'format', 'other_format', 'paper_type', 'other_paper', 'design_file', 'other_file', 'comment', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'format': forms.Select(attrs={'class':'option-select','id':'format'}),
                   'other_format': forms.TextInput(attrs={'class':'option-input','id':'other-format','placeholder':'Précisez le format'}),
                   'paper_type': forms.Select(attrs={'class':'option-select','id':'paper-type'}),
                   'other_paper': forms.TextInput(attrs={'class':'option-input','id':'other-paper','placeholder':'Précisez le type de papier'}),
                   'design_file': forms.Select(attrs={'class':'option-select','id':'design-file'}),
                   'other_file': forms.TextInput(attrs={'class':'option-input','id':'other-file','placeholder':'Précisez un autre fichier si nécessaire'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_name': forms.TextInput(attrs={'class':'form-control','id':'client-name'}),
                   'client_email': forms.EmailInput(attrs={'class':'form-control','id':'client-email'}),
                   'client_phone': forms.TextInput(attrs={'class':'form-control','id':'client-phone'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }
        
class ImpressionTextileEtVetementModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service d'impression sur textiles et vêtements, 
    pour les utilisateurs authentifiés, 
    donc les champs client ne sont pas demandés car ils sont pris depuis le compte utilisateur
    """

    class Meta:
        model = ImpressionTextileEtVetementModel
        fields = ['image', 'textile_type', 'other_textile', 'impression_type', 'design_file', 'other_design_file', 'comment', 'quantity', 'width', 'height', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'textile_type': forms.Select(attrs={'class':'option-select','id':'textile-type'}),
                   'other_textile': forms.TextInput(attrs={'class':'option-input','id':'other-textile','placeholder':'Précisez un autre textile si nécessaire', 'style':'display: none; margin-top: 0.8rem;'}),
                   'impression_type': forms.Select(attrs={'class':'option-select','id':'impression-type'}),
                   'design_file': forms.Select(attrs={'class':'option-select','id':'design-file'}),
                   'other_design_file': forms.TextInput(attrs={'class':'option-input','id':'other-file','placeholder':'Précisez un autre fichier si nécessaire', 'style':'display: none; margin-top: 0.8rem;'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }
        
class AnonymousImpressionTextileEtVetementModelForm(forms.ModelForm):
    """
    formulaire utilisé pour le service d'impression sur textiles et vêtements, 
    pour les utilisateurs non authentifiés, donc les champs client sont demandés
    """

    class Meta:
        model = ImpressionTextileEtVetementModel
        fields = ['image', 'textile_type', 'other_textile', 'impression_type', 'design_file', 'other_design_file', 'comment', 'quantity', 'width', 'height', 'client_name', 'client_email', 'client_phone', 'client_address', 'delivery_mode']
        widgets = {'image':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}), 
                   'textile_type': forms.Select(attrs={'class':'option-select','id':'textile-type'}),
                   'other_textile': forms.TextInput(attrs={'class':'option-input','id':'other-textile','placeholder':'Précisez un autre textile si nécessaire'}),
                   'impression_type': forms.Select(attrs={'class':'option-select','id':'impression-type'}),
                   'design_file': forms.Select(attrs={'class':'option-select','id':'design-file'}),
                   'other_design_file': forms.TextInput(attrs={'class':'option-input','id':'other-file','placeholder':'Précisez un autre fichier si nécessaire'}),
                   'comment': forms.Textarea(attrs={'class':'option-textarea','id':'special-notes','rows':'3','placeholder':'Ajoutez des instructions particulières (position, détails, etc.)...'}),
                   'quantity': forms.NumberInput(attrs={'class':'option-input','id':'quantity','min':'1', 'value':'1', 'style':'max-width: 80px;'}),
                   'width': forms.NumberInput(attrs={'class':'option-input','id':'width','min':'1','value':'1','min':'1', 'max': '100'}),
                   'height': forms.NumberInput(attrs={'class':'option-input','id':'height','min':'1','value':'1','min':'1', 'max': '100'}),
                   'client_name': forms.TextInput(attrs={'class':'form-control','id':'client-name'}),
                   'client_email': forms.EmailInput(attrs={'class':'form-control','id':'client-email'}),
                   'client_phone': forms.TextInput(attrs={'class':'form-control','id':'client-phone'}),
                   'client_address': forms.TextInput(attrs={'class':'form-control','id':'client-address'}),
                   'delivery_mode': forms.Select(attrs={'class':'form-control','id':'delivery-mode'})
                   }