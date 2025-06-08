from django.contrib import admin

from Services.models import Service, ClientCustomizationForBroderieNumerique, ClientCustomizationForFraiseuseNumerique, \
    ClientCustomizationForDecoupeLaser, ClientCustomizationForImpression3D, ClientCustomizationForPaper, \
    ClientCustomizationForTextile, ClientCustomizationForObjects


# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('name','description','image1','image2','image3','image4','image5','image6','image7','image8',)
    list_display = ('name','description',)

@admin.register(ClientCustomizationForBroderieNumerique)
class BroderieOrderAdmin(admin.ModelAdmin):
    fields = ('support_type', 'other_support', 'dim_1', 'dim_2', 'quantity',
                  'special_instructions', 'codeCouleur',
                  'name','email', 'tel_number','town', 'upload_design_picture','design_picture',
                  'delivery_mode', 'cgu_accept', 'service', )

    list_display = ('name','email', 'tel_number','town','service',)

@admin.register(ClientCustomizationForFraiseuseNumerique)
class FraiseuseOrderAdmin(admin.ModelAdmin):
    fields = ('service_type', 'dim_1', 'dim_2', 'quantity',
                  'special_instructions', 'used_materials',
                  'name','email', 'tel_number','town', 'upload_design_picture','design_picture',
                  'delivery_mode', 'cgu_accept', 'service', )

    list_display = ('name','email', 'tel_number','town','service',)

@admin.register(ClientCustomizationForDecoupeLaser)
class LaserOrderAdmin(admin.ModelAdmin):
    fields = ('service_type', 'dim_1', 'dim_2', 'quantity',
                  'special_instructions', 'used_materials',
                  'name','email', 'tel_number','town', 'upload_design_picture','design_picture',
                  'delivery_mode', 'cgu_accept', 'service', )

    list_display = ('name','email', 'tel_number','town','service',)

@admin.register(ClientCustomizationForImpression3D)
class Imp3DOrderAdmin(admin.ModelAdmin):
    fields = ('impression_type', 'dim_1', 'dim_2', 'quantity',
                  'special_instructions', 'used_materials','codeCouleur',
                  'name','email', 'tel_number','town', 'upload_design_picture','design_picture',
                  'delivery_mode', 'cgu_accept', 'service', )

    list_display = ('name','email', 'tel_number','town','service',)

@admin.register(ClientCustomizationForPaper)
class PaperOrderAdmin(admin.ModelAdmin):
    fields = ('wished_format'
              ,'other_format'
              ,'paper'
              ,'other_paper'
              ,'design_file'
              ,'other_design_file'
              ,'service', 'dim_1',
              'dim_2', 'quantity',
              'special_instructions', 'codeCouleur',
              'design_picture', 'upload_design_picture',
              'name', 'email', 'tel_number', 'town',
              'delivery_mode','cgu_accept',)

    list_display = ('name','email', 'tel_number','town','service',)

@admin.register(ClientCustomizationForTextile)
class TextileOrderAdmin(admin.ModelAdmin):
    fields = ('service',
            'textile_type',
            'other_textile',
            'impression_wished',
            'design_file',
            'other_design_file',
            'dim_1',
            'dim_2',
            'codeCouleur',
            'quantity',
            'special_instructions',
            'design_picture',
            'upload_design_picture',
            'name',
            'email',
            'tel_number',
            'town',
            'delivery_mode',
            'cgu_accept',)

    list_display = ('name','email', 'tel_number','town','service',)

@admin.register(ClientCustomizationForObjects)
class ObjectsOrderAdmin(admin.ModelAdmin):
    fields = (
        'service',
        'object',
        'other_object',
        'design_file',
        'other_design_file',
        'dim_1',
        'dim_2',
        'codeCouleur',
        'quantity',
        'special_instructions',
        'design_picture',
        'upload_design_picture',
        'name',
        'email',
        'tel_number',
        'town',
        'delivery_mode',
        'cgu_accept',
    )
    
    list_display = ('name','email', 'tel_number','town','service',)