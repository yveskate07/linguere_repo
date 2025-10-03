from django import forms

from Services.models import ClientCustomizationForBroderieNumerique, ClientCustomizationForFraiseuseNumerique, \
    ClientCustomizationForDecoupeLaser, ClientCustomizationForImpression3D, ClientCustomizationForPaper, \
    ClientCustomizationForTextile, ClientCustomizationForObjects, CustomizedService


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

class Broderie_num_customForm1(forms.ModelForm):
    """
    formulaire utilisé lorsque l'utilisateur choisit un design deja disponible
    """
    class Meta:
        model = ClientCustomizationForBroderieNumerique
        fields = ['support_type', 'other_support', 'dim_1', 'dim_2', 'quantity',
                  'special_instructions', 'design_picture', 'codeCouleur','town',
                  'delivery_mode', 'cgu_accept']

        widgets = {
                   'support_type':forms.Select(attrs={'id':'support-type1','class':'option-select'}),
                   'other_support':forms.TextInput(attrs={'class':"option-input", 'id':"other-support1", 
                                                          'placeholder':"Précisez le support",
                                                          'style':"display: none; margin-top: 0.8rem;"}),
                   'dim_1':forms.NumberInput(attrs={'id':'width1', 'class':"option-input", 'placeholder':"Largeur", 'min':"1", 'max':"50",'value':"10"}),
                   'dim_2':forms.NumberInput(attrs={'id':'height1', 'class':"option-input", 'placeholder':"Longueur", 'min':"1", 'max':"50",'value':"10"}),
                   'quantity':forms.NumberInput(attrs={'id':'selected-quantity1','class':"option-input",
                                                        'min':"1", 'value':"1",'style':"max-width: 80px;"}),
                   'codeCouleur':forms.TextInput(attrs={'type':"hidden", 'id':'selected-colors1'}),
                   'special_instructions':forms.TextInput(attrs={'id':'selected-notes1',
                                                                 'class':"option-textarea",
                            'placeholder':"Ajoutez des instructions particulières (position, détails, etc.)..."}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address1'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery1'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms1','class':'form-check-input'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}

    def clean_other_support(self):
        support = self.cleaned_data['support_type']
        other_support = self.cleaned_data['other_support']

        if support == "Autre (précisez)":
            if not other_support:
                raise forms.ValidationError("Autre support non precisé")

        return other_support

    def clean_codeCouleur(self):
        codeCouleur = self.cleaned_data['codeCouleur']

        if not codeCouleur:
                raise forms.ValidationError("Aucune couleur choisie")

        return codeCouleur

    def clean_design_picture(self):
        design_picture = self.cleaned_data['design_picture']

        if not design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return design_picture

class Broderie_num_customForm2(forms.ModelForm):
    """
    formulaire utilisé lorsque l'utilisateur importe un design
    """
    class Meta:
        model = ClientCustomizationForBroderieNumerique
        fields = ['support_type', 'other_support', 'dim_1', 'dim_2', 'quantity',
                  'special_instructions', 'codeCouleur','town', 'upload_design_picture',
                  'delivery_mode', 'cgu_accept']
        
        widgets = {
                   'support_type':forms.Select(attrs={'id':'support-type2','class':'option-select'}),
                   'other_support':forms.TextInput(attrs={'class':"option-input", 'id':"other-support2", 
                                                          'placeholder':"Précisez le support",
                                                          'style':"display: none; margin-top: 0.8rem;"}),
                   'dim_1':forms.NumberInput(attrs={'class':"option-input", 'id':"width2", 'placeholder':"Largeur", 'min':"1", 'max':"50",'value':"10"}),
                   'dim_2':forms.NumberInput(attrs={'class':"option-input", 'id':"height2", 'placeholder':"Longueur", 'min':"1", 'max':"50",'value':"10"}),
                   'quantity':forms.NumberInput(attrs={'id':'selected-quantity2','class':"option-input",
                                                        'min':"1", 'value':"1",'style':"max-width: 80px;"}),
                   'codeCouleur':forms.TextInput(attrs={'type':"hidden", 'id':'selected-colors2'}),
                   'special_instructions':forms.TextInput(attrs={'id':'selected-notes2',
                                                                 'class':"option-textarea",
                            'placeholder':"Ajoutez des instructions particulières (position, détails, etc.)..."}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address2'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery2'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms2','class':'form-check-input'}),
                   'upload_design_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'})}


    def clean_other_support(self):
        support = self.cleaned_data['support_type']
        other_support = self.cleaned_data['other_support']

        if support == "Autre (précisez)":
            if not other_support:
                raise forms.ValidationError("Autre support non precisé")

        return other_support

    def clean_codeCouleur(self):
        codeCouleur = self.cleaned_data['codeCouleur']

        if not codeCouleur:
                raise forms.ValidationError("Aucune couleur choisie")

        return codeCouleur

    def clean_upload_design_picture(self):
        upload_design_picture = self.cleaned_data['upload_design_picture']

        if not upload_design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return upload_design_picture

class Fraiseuse_customForm1(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur choisit un design deja disponible
    """

    class Meta:
        model = ClientCustomizationForFraiseuseNumerique
        fields = ['service_type', 'dim_1', 'dim_2', 'quantity', 'used_materials' ,
                  'special_instructions', 'design_picture','town',
                  'delivery_mode', 'cgu_accept']

        widgets = {'service_type':forms.Select(attrs={'class':"option-select" , 'id':'selected-service1'}),
                   'dim_1':forms.NumberInput(attrs={'id':'width1', 'class':"option-input", 'placeholder':"Largeur", 'value':"10"}),
                   'dim_2':forms.NumberInput(attrs={'id':'height1', 'class':"option-input", 'placeholder':"Longueur", 'value':"10"}),
                   'quantity':forms.NumberInput(attrs={'id':'quantity1', 'class':"option-input",
                                                        'min':"1", 'value':"1",'style':"max-width: 80px;"}),
                   'used_materials': forms.Select(attrs={'id': 'selected-support1', 'class':"option-select"}),
                   'special_instructions':forms.TextInput(attrs={'id':'selected-notes1', 'class':"option-textarea",
                            'placeholder':"Ajoutez des instructions particulières (position, détails, etc.)..."}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address1'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery1'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms1','class':'form-check-input'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}


    def clean_design_picture(self):
        design_picture = self.cleaned_data['design_picture']

        if not design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return design_picture
        
class Fraiseuse_customForm2(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur importe un design
    """

    class Meta:
        model = ClientCustomizationForFraiseuseNumerique
        fields = ['service_type', 'dim_1', 'dim_2', 'quantity', 'used_materials' ,
                  'special_instructions', 'upload_design_picture','town',
                  'delivery_mode', 'cgu_accept']
        
        widgets = {'service_type':forms.Select(attrs={'class':"option-select" , 'id':'selected-service2'}),
                   'dim_1':forms.NumberInput(attrs={'id':'width2', 'class':"option-input", 'placeholder':"Largeur", 'value':"10"}),
                   'dim_2':forms.NumberInput(attrs={'id':'height2', 'class':"option-input", 'placeholder':"Longueur", 'value':"10"}),
                   'quantity':forms.NumberInput(attrs={'id':'quantity2', 'class':"option-input",'min':"1", 'value':"1",'style':"max-width: 80px;"}),
                   'used_materials': forms.Select(attrs={'id': 'selected-support2', 'class':"option-select"}),
                   'special_instructions':forms.TextInput(attrs={'id':'selected-notes2', 'class':"option-textarea",'placeholder':"Ajoutez des instructions particulières (position, détails, etc.)..."}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address2'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery2'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms2','class':'form-check-input'}),
                   'upload_design_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'})}

    def clean_upload_design_picture(self):
        upload_design_picture = self.cleaned_data['upload_design_picture']

        if not upload_design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return upload_design_picture

class Laser_customForm1(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur choisit un design deja disponible
    """

    class Meta:
        model = ClientCustomizationForDecoupeLaser
        fields = ['service_type', 'dim_1', 'dim_2', 'quantity', 'used_materials' ,
                  'special_instructions', 'design_picture','town',
                  'delivery_mode', 'cgu_accept']
        
        widgets = {'service_type':forms.Select(attrs={'class':"option-select" , 'id':'selected-service1'}),
                   'dim_1':forms.NumberInput(attrs={'id':'width1', 'class':"option-input", 'placeholder':"Largeur", 'value':"10"}),
                   'dim_2':forms.NumberInput(attrs={'id':'height1', 'class':"option-input", 'placeholder':"Longueur", 'value':"10"}),
                   'quantity':forms.NumberInput(attrs={'id':'quantity1', 'class':"option-input",
                                                        'min':"1", 'value':"1",'style':"max-width: 80px;"}),
                   'used_materials': forms.Select(attrs={'id': 'selected-support1', 'class':"option-select"}),
                   'special_instructions':forms.TextInput(attrs={'id':'selected-notes1', 'class':"option-textarea",
                            'placeholder':"Ajoutez des instructions particulières (position, détails, etc.)..."}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address1'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery1'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms1','class':'form-check-input'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}

    def clean_design_picture(self):
        design_picture = self.cleaned_data['design_picture']

        if not design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return design_picture

class Laser_customForm2(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur importe un design
    """

    class Meta:
        model = ClientCustomizationForDecoupeLaser
        fields = ['service_type', 'dim_1', 'dim_2', 'quantity', 'used_materials' ,
                  'special_instructions','upload_design_picture','town',
                  'delivery_mode', 'cgu_accept']

        widgets = {'service_type':forms.Select(attrs={'class':"option-select" , 'id':'selected-service2'}),
                   'dim_1':forms.NumberInput(attrs={'id':'width2', 'class':"option-input", 'placeholder':"Largeur", 'value':"10"}),
                   'dim_2':forms.NumberInput(attrs={'id':'height2', 'class':"option-input", 'placeholder':"Longueur", 'value':"10"}),
                   'quantity':forms.NumberInput(attrs={'id':'quantity2', 'class':"option-input",'min':"1", 'value':"1",'style':"max-width: 80px;"}),
                   'used_materials': forms.Select(attrs={'id': 'selected-support2', 'class':"option-select"}),
                   'special_instructions':forms.TextInput(attrs={'id':'selected-notes2', 'class':"option-textarea",'placeholder':"Ajoutez des instructions particulières (position, détails, etc.)..."}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address2'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery2'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms2','class':'form-check-input'}),
                   'upload_design_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'})}

    def clean_upload_design_picture(self):
        upload_design_picture = self.cleaned_data['upload_design_picture']

        if not upload_design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return upload_design_picture

class Imp_3D_customForm1(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur choisit un design deja disponible
    """

    class Meta:
        model = ClientCustomizationForImpression3D
        fields = ['impression_type', 'dim_1', 'dim_2', 'quantity', 'codeCouleur', 'used_materials' ,
                  'special_instructions', 'design_picture','town',
                  'delivery_mode', 'cgu_accept']

        widgets = {'impression_type':forms.Select(attrs={'class':"option-select", 'id':'selected-impression1'}),
                   'dim_1':forms.NumberInput(attrs={'id':'width1', 'class':"option-input", 'placeholder':"Largeur", 'value':"10"}),
                   'dim_2':forms.NumberInput(attrs={'id':'height1', 'class':"option-input", 'placeholder':"Longueur", 'value':"10"}),
                   'codeCouleur':forms.TextInput(attrs={'type':"hidden", 'id':'selected-colors1'}),
                   'quantity':forms.NumberInput(attrs={'id':'quantity1', 'class':"option-input",'min':"1", 'value':"1",'style':"max-width: 80px;"}),
                   'used_materials': forms.Select(attrs={'id': 'selected-support1', 'class':"option-select"}),
                   'special_instructions':forms.TextInput(attrs={'id':'selected-notes1', 'class':"option-textarea",'placeholder':"Ajoutez des instructions particulières (position, détails, etc.)..."}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address1'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery1'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms1','class':'form-check-input'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}

    def clean_design_picture(self):
        design_picture = self.cleaned_data['design_picture']

        if not design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return design_picture

class Imp_3D_customForm2(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur importe un design
    """

    class Meta:
        model = ClientCustomizationForImpression3D
        fields = ['impression_type', 'dim_1', 'dim_2', 'quantity', 'codeCouleur', 'used_materials' ,
                  'special_instructions', 'upload_design_picture','town',
                  'delivery_mode', 'cgu_accept']

        widgets = {'impression_type': forms.Select(attrs={'class': "option-select", 'id': 'selected-impression2'}),
                   'dim_1': forms.NumberInput(
                       attrs={'id': 'width2', 'class': "option-input", 'placeholder': "Largeur", 'value': "10"}),
                   'dim_2': forms.NumberInput(
                       attrs={'id': 'height2', 'class': "option-input", 'placeholder': "Longueur", 'value': "10"}),
                   'codeCouleur': forms.TextInput(attrs={'type': "hidden", 'id': 'selected-colors2'}),
                   'quantity': forms.NumberInput(
                       attrs={'id': 'quantity2', 'class': "option-input", 'min': "1", 'value': "1",
                              'style': "max-width: 80px;"}),
                   'used_materials': forms.Select(attrs={'id': 'selected-support2', 'class': "option-select"}),
                   'special_instructions': forms.TextInput(attrs={'id': 'selected-notes2', 'class': "option-textarea",
                                                                  'placeholder': "Ajoutez des instructions particulières (position, détails, etc.)..."}),
                   'town': forms.TextInput(attrs={'class': 'form-control', 'id': 'address2'}),
                   'delivery_mode': forms.Select(attrs={'class': 'form-control', 'id': 'delivery2'}),
                   'cgu_accept': forms.CheckboxInput(attrs={'id': 'terms2', 'class': 'form-check-input'}),
                   'upload_design_picture': forms.ClearableFileInput(
                       attrs={'id': 'file-input', 'style': 'display: none;'})}

    def clean_upload_design_picture(self):
        upload_design_picture = self.cleaned_data['upload_design_picture']

        if not upload_design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return upload_design_picture

class Paper_customForm1(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur choisit un design deja disponible
    """

    class Meta:
        model = ClientCustomizationForPaper
        fields = [
            'wished_format', 'other_format','paper','other_paper','design_file','other_design_file',
            'dim_1','dim_2','codeCouleur','quantity','special_instructions',
            'design_picture','town','delivery_mode','cgu_accept'
        ]

        widgets = {
            'wished_format': forms.Select(attrs={
                'id': 'format-select1', 
                'class': 'option-select'
            }),
            'other_format': forms.TextInput(attrs={
                'id': 'other-format1', 
                'class': 'option-input', 
                'placeholder': 'Précisez le support', 
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'paper': forms.Select(attrs={
                'id': 'type-paper1', 
                'class': 'option-select'
            }),
            'other_paper': forms.TextInput(attrs={
                'id': 'other-type-paper1', 
                'class': 'option-input', 
                'placeholder': 'Précisez le matériau', 
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'design_file': forms.Select(attrs={
                'id': 'design-file1', 
                'class': 'option-select'
            }),
            'other_design_file': forms.TextInput(attrs={
                'id': 'other-design-file1', 
                'class': 'option-input', 
                'placeholder': 'Précisez le type de fichier', 
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'dim_1': forms.NumberInput(attrs={
                'id': 'width1', 
                'class': 'option-input', 
                'placeholder': 'Largeur', 
                'min': '1', 
                'max': '50', 
                'value': '10'
            }),
            'dim_2': forms.NumberInput(attrs={
                'id': 'height1', 
                'class': 'option-input', 
                'placeholder': 'Hauteur', 
                'min': '1', 
                'max': '50', 
                'value': '10'
            }),
            'codeCouleur': forms.TextInput(attrs={
                'id': 'selected-colors1',
                'type': 'hidden'
            }),
            'quantity': forms.NumberInput(attrs={
                'id': 'quantity1', 
                'class': 'option-input', 
                'min': '1', 
                'value': '1', 
                'style': 'max-width: 80px;'
            }),
            'special_instructions': forms.Textarea(attrs={
                'id': 'special-notes1', 
                'class': 'option-textarea', 
                'placeholder': 'Ajoutez des instructions particulières (position, détails, etc.)...'
            }),
            'town': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'address1',
                'required': True
            }),
            'delivery_mode': forms.Select(attrs={
                'class': 'form-control', 
                'id': 'delivery1', 
                'required': True
            }),
            'cgu_accept': forms.CheckboxInput(attrs={
                'id': 'terms1', 
                'class': 'form-check-input', 
                'required': True
            }),
            'design_picture': forms.TextInput(attrs={
                'id': 'selected-design', 
                'type': 'hidden'
            }),
        }

    def clean_design_picture(self):
        design_picture = self.cleaned_data['design_picture']

        if not design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return design_picture

    def clean_codeCouleur(self):
        codeCouleur = self.cleaned_data['codeCouleur']

        if not codeCouleur:
                raise forms.ValidationError("Aucune couleur choisie")

        return codeCouleur

    def clean_other_format(self):
        wished_format = self.cleaned_data['wished_format']
        other_format = self.cleaned_data['other_format']

        if wished_format == "Autre (précisez)":
            if not other_format:
                raise forms.ValidationError("Autre format non precisé")

        return other_format

    def clean_other_paper(self):
        paper = self.cleaned_data['paper']
        other_paper = self.cleaned_data['other_paper']

        if paper == "Autre (précisez)":
            if not other_paper:
                raise forms.ValidationError("Autre papier non precisé")

        return other_paper

    def clean_other_design_file(self):
        design_file = self.cleaned_data['design_file']
        other_design_file = self.cleaned_data['other_design_file']

        if design_file == "Autre (précisez)":
            if not other_design_file:
                raise forms.ValidationError("Autre fichier de design non precisé")

        return other_design_file

class Paper_customForm2(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur importe un design
    """

    class Meta:
        model = ClientCustomizationForPaper
        fields = [
            'wished_format', 'other_format','paper','other_paper','design_file','other_design_file',
            'dim_1','dim_2','codeCouleur','quantity','special_instructions',
            'upload_design_picture','town','delivery_mode','cgu_accept'
        ]

        widgets = {
            'wished_format': forms.Select(attrs={
                'id': 'format-select2', 
                'class': 'option-select'
            }),
            'other_format': forms.TextInput(attrs={
                'id': 'other-format2', 
                'class': 'option-input', 
                'placeholder': 'Précisez le support', 
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'paper': forms.Select(attrs={
                'id': 'type-paper2', 
                'class': 'option-select'
            }),
            'other_paper': forms.TextInput(attrs={
                'id': 'other-type-paper2', 
                'class': 'option-input', 
                'placeholder': 'Précisez le matériau', 
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'design_file': forms.Select(attrs={
                'id': 'design-file2', 
                'class': 'option-select'
            }),
            'other_design_file': forms.TextInput(attrs={
                'id': 'other-design-file2', 
                'class': 'option-input', 
                'placeholder': 'Précisez le type de fichier', 
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'dim_1': forms.NumberInput(attrs={
                'id': 'width2', 
                'class': 'option-input', 
                'placeholder': 'Largeur', 
                'min': '1', 
                'max': '50', 
                'value': '10'
            }),
            'dim_2': forms.NumberInput(attrs={
                'id': 'height2', 
                'class': 'option-input', 
                'placeholder': 'Hauteur', 
                'min': '1', 
                'max': '50', 
                'value': '10'
            }),
            'codeCouleur': forms.TextInput(attrs={
                'id': 'selected-colors2',
                'type': 'hidden'
            }),
            'quantity': forms.NumberInput(attrs={
                'id': 'quantity2', 
                'class': 'option-input', 
                'min': '1', 
                'value': '1', 
                'style': 'max-width: 80px;'
            }),
            'special_instructions': forms.Textarea(attrs={
                'id': 'special-notes2', 
                'class': 'option-textarea', 
                'placeholder': 'Ajoutez des instructions particulières (position, détails, etc.)...'
            }),
            'town': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'address2',
                'required': True
            }),
            'delivery_mode': forms.Select(attrs={
                'class': 'form-control', 
                'id': 'delivery2', 
                'required': True
            }),
            'cgu_accept': forms.CheckboxInput(attrs={
                'id': 'terms2', 
                'class': 'form-check-input', 
                'required': True
            }),
            'upload_design_picture': forms.ClearableFileInput(
                       attrs={'id': 'file-input', 'style': 'display: none;'}),
        }

    def clean_codeCouleur(self):
        codeCouleur = self.cleaned_data['codeCouleur']

        if not codeCouleur:
                raise forms.ValidationError("Aucune couleur choisie")

        return codeCouleur

    def clean_other_format(self):
        wished_format = self.cleaned_data['wished_format']
        other_format = self.cleaned_data['other_format']

        if wished_format == "Autre (précisez)":
            if not other_format:
                raise forms.ValidationError("Autre format non precisé")

        return other_format

    def clean_other_paper(self):
        paper = self.cleaned_data['paper']
        other_paper = self.cleaned_data['other_paper']

        if paper == "Autre (précisez)":
            if not other_paper:
                raise forms.ValidationError("Autre papier non precisé")

        return other_paper

    def clean_other_design_file(self):
        design_file = self.cleaned_data['design_file']
        other_design_file = self.cleaned_data['other_design_file']

        if design_file == "Autre (précisez)":
            if not other_design_file:
                raise forms.ValidationError("Autre fichier de design non precisé")

        return other_design_file

    def clean_upload_design_picture(self):
        upload_design_picture = self.cleaned_data['upload_design_picture']

        if not upload_design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return upload_design_picture

class Textile_customForm1(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur choisit un design deja disponible"""

    class Meta:
        model = ClientCustomizationForTextile
        fields = [
            'textile_type', 'other_textile', 'other_design_file',
            'design_file', 'impression_wished', 'dim_1', 'dim_2', 'codeCouleur',
            'quantity', 'special_instructions', 'design_picture', 'town', 'delivery_mode', 'cgu_accept'
        ]

        widgets = {
            'textile_type': forms.Select(attrs={
                'id': 'textile-type1',
                'class': 'option-select'
            }),
            'other_textile': forms.TextInput(attrs={
                'id': 'other-textile1',
                'class': 'option-input',
                'placeholder': 'Précisez le support',
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'design_file': forms.Select(attrs={
                'id': 'design-file1',
                'class': 'option-select'
            }),
            'other_design_file': forms.TextInput(attrs={
                'id': 'other-design-file1',
                'class': 'option-input',
                'placeholder': 'Précisez le type de fichier',
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'impression_wished': forms.Select(attrs={
                'id': 'impression-type1',
                'class': 'option-select'
            }),
            'dim_1': forms.NumberInput(attrs={
                'id': 'width1',
                'class': 'option-input',
                'placeholder': 'Largeur',
                'min': '1',
                'max': '50',
                'value': '10'
            }),
            'dim_2': forms.NumberInput(attrs={
                'id': 'height1',
                'class': 'option-input',
                'placeholder': 'Hauteur',
                'min': '1',
                'max': '50',
                'value': '10'
            }),
            'codeCouleur': forms.TextInput(attrs={
                'id': 'selected-colors1',
                'type': 'hidden'
            }),
            'quantity': forms.NumberInput(attrs={
                'id': 'quantity1',
                'class': 'option-input',
                'min': '1',
                'value': '1',
                'style': 'max-width: 80px;'
            }),
            'special_instructions': forms.Textarea(attrs={
                'id': 'special-notes1',
                'class': 'option-textarea',
                'placeholder': 'Ajoutez des instructions particulières (position, détails, etc.)...'
            }),
            'town': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'address1',
                'required': True
            }),
            'delivery_mode': forms.Select(attrs={
                'class': 'form-control',
                'id': 'delivery1',
                'required': True
            }),
            'cgu_accept': forms.CheckboxInput(attrs={
                'id': 'terms1',
                'class': 'form-check-input',
                'required': True
            }),
            'design_picture': forms.TextInput(attrs={
                'id': 'selected-design',
                'type': 'hidden'
            })
        }

    def clean_codeCouleur(self):
        codeCouleur = self.cleaned_data['codeCouleur']

        if not codeCouleur:
                raise forms.ValidationError("Aucune couleur choisie")

        return codeCouleur

    def clean_other_textile(self):
        textile_type = self.cleaned_data['textile_type']
        other_textile = self.cleaned_data['other_textile']

        if textile_type == "Autre (précisez)":
            if not other_textile:
                raise forms.ValidationError("Autre textile non precisé")

        return other_textile

    def clean_other_design_file(self):
        design_file = self.cleaned_data['design_file']
        other_design_file = self.cleaned_data['other_design_file']

        if design_file == "Autre (précisez)":
            if not other_design_file:
                raise forms.ValidationError("Autre fichier de design non precisé")

        return other_design_file

    def clean_design_picture(self):
        design_picture = self.cleaned_data['design_picture']

        if not design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return design_picture

class Textile_customForm2(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur importe un design"""

    class Meta:
        model = ClientCustomizationForTextile
        fields = [
            'textile_type', 'other_textile', 'other_design_file',
            'design_file', 'impression_wished', 'dim_1', 'dim_2', 'codeCouleur',
            'quantity', 'special_instructions', 'upload_design_picture', 'town', 'delivery_mode', 'cgu_accept'
        ]

        widgets = {
            'textile_type': forms.Select(attrs={
                'id': 'textile-type2',
                'class': 'option-select'
            }),
            'other_textile': forms.TextInput(attrs={
                'id': 'other-textile2',
                'class': 'option-input',
                'placeholder': 'Précisez le support',
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'design_file': forms.Select(attrs={
                'id': 'design-file2',
                'class': 'option-select'
            }),
            'other_design_file': forms.TextInput(attrs={
                'id': 'other-design-file2',
                'class': 'option-input',
                'placeholder': 'Précisez le type de fichier',
                'style': 'display: none; margin-top: 0.8rem;'
            }),
            'impression_wished': forms.Select(attrs={
                'id': 'impression-type2',
                'class': 'option-select'
            }),
            'dim_1': forms.NumberInput(attrs={
                'id': 'width2',
                'class': 'option-input',
                'placeholder': 'Largeur',
                'min': '1',
                'max': '50',
                'value': '10'
            }),
            'dim_2': forms.NumberInput(attrs={
                'id': 'height2',
                'class': 'option-input',
                'placeholder': 'Hauteur',
                'min': '1',
                'max': '50',
                'value': '10'
            }),
            'codeCouleur': forms.TextInput(attrs={
                'id': 'selected-colors2',
                'type': 'hidden'
            }),
            'quantity': forms.NumberInput(attrs={
                'id': 'quantity2',
                'class': 'option-input',
                'min': '1',
                'value': '1',
                'style': 'max-width: 80px;'
            }),
            'special_instructions': forms.Textarea(attrs={
                'id': 'special-notes2',
                'class': 'option-textarea',
                'placeholder': 'Ajoutez des instructions particulières (position, détails, etc.)...'
            }),
            'town': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'address2',
                'required': True
            }),
            'delivery_mode': forms.Select(attrs={
                'class': 'form-control',
                'id': 'delivery2',
                'required': True
            }),
            'cgu_accept': forms.CheckboxInput(attrs={
                'id': 'terms2',
                'class': 'form-check-input',
                'required': True
            }),
            'upload_design_picture': forms.ClearableFileInput(
                       attrs={'id': 'file-input', 'style': 'display: none;'})
        }

    def clean_codeCouleur(self):
        codeCouleur = self.cleaned_data['codeCouleur']

        if not codeCouleur:
                raise forms.ValidationError("Aucune couleur choisie")

        return codeCouleur

    def clean_other_textile(self):
        textile_type = self.cleaned_data['textile_type']
        other_textile = self.cleaned_data['other_textile']

        if textile_type == "Autre (précisez)":
            if not other_textile:
                raise forms.ValidationError("Autre textile non precisé")

        return other_textile

    def clean_other_design_file(self):
        design_file = self.cleaned_data['design_file']
        other_design_file = self.cleaned_data['other_design_file']

        if design_file == "Autre (précisez)":
            if not other_design_file:
                raise forms.ValidationError("Autre fichier de design non precisé")

        return other_design_file

    def clean_upload_design_picture(self):
        upload_design_picture = self.cleaned_data['upload_design_picture']

        if not upload_design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return upload_design_picture

class Objects_customForm1(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur choisit un design deja disponible
    """

    class Meta:
        model = ClientCustomizationForObjects
        fields = ['object', 'other_object',
                  'design_file', 'other_design_file',
                  'dim_1', 'dim_2', 'codeCouleur',
                  'quantity', 'special_instructions',
                  'design_picture', 'town',
                  'delivery_mode', 'cgu_accept']

        widgets = {
            'object': forms.Select(attrs={
                'class': 'option-select',
                'id': 'support-type1'
            }),
            'other_object': forms.TextInput(attrs={
                'type': 'text', 'class': 'option-input', 'id': 'other-support1',
                'placeholder': 'Précisez le support', 'style': 'display: none; margin-top: 0.8rem;'
            }),
            'design_file': forms.Select(attrs={
                'class': 'option-select', 'id': 'design-file1'
            }),
            'other_design_file': forms.TextInput(attrs={
                'type': 'text', 'class': 'option-input', 'id': 'other-design-file1',

                'placeholder': 'Précisez le type de fichier', 'style': 'display: none; margin-top: 0.8rem;'
            }),
            'dim_1': forms.NumberInput(attrs={
                'type': 'number', 'class': 'option-input', 'id': 'width1',
                'placeholder': 'Largeur', 'min': '1', 'max': '50', 'value': '10'
            }),
            'dim_2': forms.NumberInput(attrs={
                'type': 'number', 'class': 'option-input', 'id': 'height1',
                'placeholder': 'Hauteur', 'min': '1', 'max': '50', 'value': '10'
            }),
            'codeCouleur': forms.TextInput(attrs={
                'type': 'hidden', 'id': 'selected-colors1'
            }),
            'quantity': forms.NumberInput(attrs={
                'type': 'number', 'class': 'option-input', 'id': 'quantity1',
                'min': '1', 'value': '1', 'style': 'max-width: 80px;'
            }),
            'special_instructions': forms.Textarea(attrs={
                'class': 'option-textarea', 'id': 'special-notes1',
                'placeholder': 'Ajoutez des instructions particulières (position, détails, etc.)...'
            }),
            'town': forms.TextInput(attrs={
                'type': 'text', 'id': 'address1',
                'name': 'address', 'required': True, 'class': 'form-control'
            }),
            'delivery_mode': forms.Select(attrs={
                'id': 'delivery1',
                'name': 'delivery', 'required': True, 'class': 'form-control'
            }),
            'cgu_accept': forms.CheckboxInput(attrs={
                'type': 'checkbox', 'id': 'terms1',
                'name': 'terms', 'required': True, 'class': 'form-check-input'
            }),
            'design_picture': forms.TextInput(attrs={
                'id': 'selected-design',
                'type': 'hidden'
            })
        }

    def clean_design_picture(self):
        design_picture = self.cleaned_data['design_picture']

        if not design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return design_picture

    def clean_codeCouleur(self):
        codeCouleur = self.cleaned_data['codeCouleur']

        if not codeCouleur:
            raise forms.ValidationError("Aucune couleur choisie")

        return codeCouleur

    def clean_other_design_file(self):
        design_file = self.cleaned_data['design_file']
        other_design_file = self.cleaned_data['other_design_file']

        if design_file == "Autre (précisez)":
            if not other_design_file:
                raise forms.ValidationError("Autre fichier de design non precisé")

        return other_design_file

    def clean_other_object(self):
        object = self.cleaned_data['object']
        other_object = self.cleaned_data['other_object']

        if object == "Autre (précisez)":
            if not other_object:
                raise forms.ValidationError("Autre objet non precisé")

        return other_object

class Objects_customForm2(forms.ModelForm):

    """
    formulaire utilisé lorsque l'utilisateur importe un design
    """

    class Meta:
        model = ClientCustomizationForObjects
        fields = ['object', 'other_object',
                  'design_file', 'other_design_file',
                  'dim_1', 'dim_2', 'codeCouleur',
                  'quantity', 'special_instructions',
                  'upload_design_picture', 'town',
                  'delivery_mode', 'cgu_accept']

        widgets = {
            'object': forms.Select(attrs={
                'class': 'option-select',
                'id': 'support-type2'
            }),
            'other_object': forms.TextInput(attrs={
                'type': 'text', 'class': 'option-input', 'id': 'other-support2',
                'placeholder': 'Précisez le support', 'style': 'display: none; margin-top: 0.8rem;'
            }),
            'design_file': forms.Select(attrs={
                'class': 'option-select', 'id': 'design-file2'
            }),
            'other_design_file': forms.TextInput(attrs={
                'type': 'text', 'class': 'option-input', 'id': 'other-design-file2',

                'placeholder': 'Précisez le type de fichier', 'style': 'display: none; margin-top: 0.8rem;'
            }),
            'dim_1': forms.NumberInput(attrs={
                'type': 'number', 'class': 'option-input', 'id': 'width2',
                'placeholder': 'Largeur', 'min': '1', 'max': '50', 'value': '10'
            }),
            'dim_2': forms.NumberInput(attrs={
                'type': 'number', 'class': 'option-input', 'id': 'height2',
                'placeholder': 'Hauteur', 'min': '1', 'max': '50', 'value': '10'
            }),
            'codeCouleur': forms.TextInput(attrs={
                'type': 'hidden', 'id': 'selected-colors2'
            }),
            'quantity': forms.NumberInput(attrs={
                'type': 'number', 'class': 'option-input', 'id': 'quantity2',
                'min': '1', 'value': '1', 'style': 'max-width: 80px;'
            }),
            'special_instructions': forms.Textarea(attrs={
                'class': 'option-textarea', 'id': 'special-notes2',
                'placeholder': 'Ajoutez des instructions particulières (position, détails, etc.)...'
            }),
            'town': forms.TextInput(attrs={
                'type': 'text', 'id': 'address2',
                'name': 'address', 'required': True, 'class': 'form-control'
            }),
            'delivery_mode': forms.Select(attrs={
                'id': 'delivery2',
                'name': 'delivery', 'required': True, 'class': 'form-control'
            }),
            'cgu_accept': forms.CheckboxInput(attrs={
                'type': 'checkbox', 'id': 'terms2',
                'name': 'terms', 'required': True, 'class': 'form-check-input'
            }),
            'upload_design_picture': forms.ClearableFileInput(attrs={
                'id': 'file-input', 'style': 'display: none;'
            })
        }

    def clean_upload_design_picture(self):
        upload_design_picture = self.cleaned_data['upload_design_picture']

        if not upload_design_picture:
            raise forms.ValidationError("Aucune image design n'a été choisie")

        return upload_design_picture

    def clean_codeCouleur(self):
        codeCouleur = self.cleaned_data['codeCouleur']

        if not codeCouleur:
                raise forms.ValidationError("Aucune couleur choisie")

        return codeCouleur

    def clean_other_design_file(self):
        design_file = self.cleaned_data['design_file']
        other_design_file = self.cleaned_data['other_design_file']

        if design_file == "Autre (précisez)":
            if not other_design_file:
                raise forms.ValidationError("Autre fichier de design non precisé")

        return other_design_file

    def clean_other_object(self):
        object = self.cleaned_data['object']
        other_object = self.cleaned_data['other_object']

        if object == "Autre (précisez)":
            if not other_object:
                raise forms.ValidationError("Autre objet non precisé")

        return other_object