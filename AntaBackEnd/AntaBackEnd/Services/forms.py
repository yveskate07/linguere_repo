from django import forms

from Services.models import ClientCustomizationForBroderieNumerique, ClientCustomizationForFraiseuseNumerique, \
    ClientCustomizationForDecoupeLaser, ClientCustomizationForImpression3D, ClientCustomizationForImpreNum


class Broderie_num_customForm(forms.ModelForm):
    class Meta:
        model = ClientCustomizationForBroderieNumerique
        fields = ['support_type', 'dim_1', 'dim_2', 'quantity',
                  'special_instructions', 'design_picture', 'codeCouleur',
                  'name','email', 'tel_number','town', 'upload_design_picture',
                  'delivery_mode', 'cgu_accept']

        widgets = {'support_type':forms.TextInput(attrs={'type':'hidden', 'id':'selected-support'}),
                   'dim_1':forms.NumberInput(attrs={'type':"hidden", 'id':'first-dimension-selected'}),
                   'dim_2':forms.NumberInput(attrs={'type':"hidden", 'id':'second-dimension-selected'}),
                   'quantity':forms.NumberInput(attrs={'type':"hidden", 'id':'selected-quantity'}),
                   'codeCouleur':forms.TextInput(attrs={'type':"hidden", 'id':'selected-colors'}),
                   'special_instructions':forms.TextInput(attrs={'type':"hidden", 'id':'selected-notes'}),
                   'name':forms.TextInput(attrs={'class':'form-control','id':'fullname'}),
                   'email':forms.EmailInput(attrs={'class':'form-control', 'id':'email'}),
                   'tel_number':forms.TextInput(attrs={'class':'form-control','id':'phone'}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms','class':'form-check-input'}),
                   'upload_design_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}

class Fraiseuse_customForm(forms.ModelForm):
    class Meta:
        model = ClientCustomizationForFraiseuseNumerique
        fields = ['service_type', 'dim_1', 'dim_2', 'quantity', 'used_materials' ,
                  'special_instructions', 'design_picture', 'upload_design_picture',
                  'name','email', 'tel_number','town',
                  'delivery_mode', 'cgu_accept']

        widgets = {'service_type':forms.TextInput(attrs={'type':'hidden', 'id':'selected-support'}),
                   'dim_1':forms.NumberInput(attrs={'type':"hidden", 'id':'first-dimension-selected'}),
                   'dim_2':forms.NumberInput(attrs={'type':"hidden", 'id':'second-dimension-selected'}),
                   'quantity':forms.NumberInput(attrs={'type':"hidden", 'id':'selected-quantity'}),
                   'used_materials': forms.TextInput(attrs={'type': 'hidden', 'id': 'selected-support'}),
                   'special_instructions':forms.TextInput(attrs={'type':"hidden", 'id':'selected-notes'}),
                   'name':forms.TextInput(attrs={'class':'form-control','id':'fullname'}),
                   'email':forms.EmailInput(attrs={'class':'form-control', 'id':'email'}),
                   'tel_number':forms.TextInput(attrs={'class':'form-control','id':'phone'}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms','class':'form-check-input'}),
                   'upload_design_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}

class Laser_customForm(forms.ModelForm):
    class Meta:
        model = ClientCustomizationForDecoupeLaser
        fields = ['service_type', 'dim_1', 'dim_2', 'quantity', 'used_materials' ,
                  'special_instructions', 'design_picture', 'upload_design_picture',
                  'name','email', 'tel_number','town',
                  'delivery_mode', 'cgu_accept']

        widgets = {'service_type':forms.TextInput(attrs={'type':'hidden', 'id':'selected-support'}),
                   'dim_1':forms.NumberInput(attrs={'type':"hidden", 'id':'first-dimension-selected'}),
                   'dim_2':forms.NumberInput(attrs={'type':"hidden", 'id':'second-dimension-selected'}),
                   'quantity':forms.NumberInput(attrs={'type':"hidden", 'id':'selected-quantity'}),
                   'used_materials': forms.TextInput(attrs={'type': 'hidden', 'id': 'selected-support'}),
                   'special_instructions':forms.TextInput(attrs={'type':"hidden", 'id':'selected-notes'}),
                   'name':forms.TextInput(attrs={'class':'form-control','id':'fullname'}),
                   'email':forms.EmailInput(attrs={'class':'form-control', 'id':'email'}),
                   'tel_number':forms.TextInput(attrs={'class':'form-control','id':'phone'}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms','class':'form-check-input'}),
                   'upload_design_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}

class Imp_3D_customForm(forms.ModelForm):
    class Meta:
        model = ClientCustomizationForImpression3D
        fields = ['impression_type', 'dim_1', 'dim_2', 'quantity', 'codeCouleur', 'used_materials' ,
                  'special_instructions', 'design_picture', 'upload_design_picture',
                  'name','email', 'tel_number','town',
                  'delivery_mode', 'cgu_accept']

        widgets = {'impression_type':forms.TextInput(attrs={'type':'hidden', 'id':'selected-support'}),
                   'dim_1':forms.NumberInput(attrs={'type':"hidden", 'id':'first-dimension-selected'}),
                   'dim_2':forms.NumberInput(attrs={'type':"hidden", 'id':'second-dimension-selected'}),
                   'codeCouleur':forms.TextInput(attrs={'type':"hidden", 'id':'selected-colors'}),
                   'quantity':forms.NumberInput(attrs={'type':"hidden", 'id':'selected-quantity'}),
                   'used_materials': forms.TextInput(attrs={'type': 'hidden', 'id': 'selected-support'}),
                   'special_instructions':forms.TextInput(attrs={'type':"hidden", 'id':'selected-notes'}),
                   'name':forms.TextInput(attrs={'class':'form-control','id':'fullname'}),
                   'email':forms.EmailInput(attrs={'class':'form-control', 'id':'email'}),
                   'tel_number':forms.TextInput(attrs={'class':'form-control','id':'phone'}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms','class':'form-check-input'}),
                   'upload_design_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}

class Imp_Num_customForm(forms.ModelForm):
    class Meta:
        model = ClientCustomizationForImpreNum
        fields = ['wished_format','paper'
                 ,'textile','design_file','support_type'
                 ,'impression_type','dim_1','dim_2','codeCouleur'
                 ,'quantity','special_instructions'
                 ,'design_picture','upload_design_picture',
                  'name','email',
                  'tel_number','town',
                  'delivery_mode','cgu_accept']

        widgets = {'wished_format': forms.TextInput(attrs={'type': 'hidden', 'id': 'selected-format'}),
                   'paper': forms.TextInput(attrs={'type': 'hidden', 'id': 'selected-paper'}),
                   'textile': forms.TextInput(attrs={'type': 'hidden', 'id': 'selected-textile'}),
                   'design_file': forms.TextInput(attrs={'type': 'hidden', 'id': 'selected-design_file'}),
                   'support_type':forms.TextInput(attrs={'type':'hidden', 'id':'selected-support'}),
                   'impression_type':forms.TextInput(attrs={'type':'hidden', 'id':'selected-support'}),
                   'dim_1':forms.NumberInput(attrs={'type':"hidden", 'id':'first-dimension-selected'}),
                   'dim_2':forms.NumberInput(attrs={'type':"hidden", 'id':'second-dimension-selected'}),
                   'codeCouleur':forms.TextInput(attrs={'type':"hidden", 'id':'selected-colors'}),
                   'quantity':forms.NumberInput(attrs={'type':"hidden", 'id':'selected-quantity'}),
                   'used_materials': forms.TextInput(attrs={'type': 'hidden', 'id': 'selected-support'}),
                   'special_instructions':forms.TextInput(attrs={'type':"hidden", 'id':'selected-notes'}),
                   'name':forms.TextInput(attrs={'class':'form-control','id':'fullname'}),
                   'email':forms.EmailInput(attrs={'class':'form-control', 'id':'email'}),
                   'tel_number':forms.TextInput(attrs={'class':'form-control','id':'phone'}),
                   'town':forms.TextInput(attrs={'class':'form-control','id':'address'}),
                   'delivery_mode':forms.Select(attrs={'class':'form-control','id':'delivery'}),
                   'cgu_accept':forms.CheckboxInput(attrs={'id':'terms','class':'form-check-input'}),
                   'upload_design_picture':forms.ClearableFileInput(attrs={'id': 'file-input','style': 'display: none;'}),
                   'design_picture':forms.TextInput(attrs={'id':'selected-design', 'type':'hidden'})}