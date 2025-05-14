from django.db import models
from .validators import validate_file_size, validate_file_extension

# Create your models here.
class Service(models.Model):


    name = models.CharField(max_length=60, verbose_name='Nom')
    description = models.TextField(verbose_name='Description')
    image1 = models.ImageField(blank=True,null=True,upload_to='Services/service_image', default='Services/service_image/default3.png', verbose_name='Image 1')
    image2 = models.ImageField(blank=True,null=True,upload_to='Services/service_image', default='Services/service_image/default3.png', verbose_name='Image 2')
    image3 = models.ImageField(blank=True,null=True,upload_to='Services/service_image', default='Services/service_image/default3.png', verbose_name='Image 3')
    image4 = models.ImageField(blank=True,null=True,upload_to='Services/service_image', default='Services/service_image/default3.png', verbose_name='Image 4')
    image5 = models.ImageField(blank=True, null=True, upload_to='Services/service_image', default='Services/service_image/default3.png', verbose_name='Image 5')
    image6 = models.ImageField(blank=True, null=True, upload_to='Services/service_image', default='Services/service_image/default3.png', verbose_name='Image 6')
    image7 = models.ImageField(blank=True, null=True, upload_to='Services/service_image', default='Services/service_image/default3.png', verbose_name='Image 7')
    image8 = models.ImageField(blank=True, null=True, upload_to='Services/service_image', default='Services/service_image/default3.png', verbose_name='Image 8')


class ClientCustomizationForBroderieNumerique(models.Model):

    LIVRAISON = [("Retrait sur place Dakar", "Retrait sur place Dakar"),
                 ("Livraison à domicile (Dakar)", "Livraison à domicile (Dakar)"),
                 ("Livraison à domicile (Autres régions)", "Livraison à domicile (Autres régions)")]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Service')

    support_type = models.CharField(blank=True, null=True, verbose_name='Type de support', max_length=30)
    dim_1 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 2')
    quantity = models.IntegerField(verbose_name='Quantité', blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    design_picture = models.CharField(verbose_name="Image du design", blank=True, null=True, max_length=60)
    upload_design_picture = models.ImageField(verbose_name="Design uploadé", upload_to="Services/uploaded_design", blank=True, null=True, validators=[validate_file_size, validate_file_extension])
    codeCouleur = models.CharField(max_length=20, blank=True,null=True, verbose_name='Code couleur')

    name = models.CharField(max_length=30, verbose_name="Nom complet")
    email = models.EmailField(max_length=50, verbose_name="Adresse mail")
    tel_number = models.CharField(blank=True, null=True, max_length=50, verbose_name="Numéro de téléphone")

    town = models.CharField(blank=True, null=True, max_length=60, verbose_name="Adresse (ville)")
    delivery_mode = models.CharField(blank=True, null=True, max_length=50, choices=LIVRAISON, verbose_name="Mode de livraison")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité")

"""

class ClientCustomizationForFraiseuseNumerique(models.Model):

    SUPPORTS = [("T-shirt", "T-shirt"),
                ("Laoste", "Laoste"),
                ("Casquette", "Casquette"),
                ("Polo", "Polo"),
                ("Sweat a capuche", "Sweat a capuche"),
                ("Serviette", "Serviette"),
                ("Sac", "Sac"),
                ("Autre (précisez)", "Autre (précisez)")]

    service_type = models.CharField(blank=True, null=True, choices=SUPPORTS, verbose_name='Type de service',
                                    max_length=30)
    dim_1 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 2')
    used_materials = models.CharField(blank=True, null=True, max_length=30, verbose_name='Materiau utilisé')
    quantity = models.IntegerField(verbose_name='Quantité', blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    name = models.CharField(max_length=30, verbose_name="Nom complet")
    email = models.EmailField(max_length=50, verbose_name="Adresse mail")
    tel_number = models.CharField(blank=True, null=True, max_length=50, verbose_name="Numéro de téléphone")

    town = models.CharField(blank=True, null=True, max_length=60, verbose_name="Adresse (ville)")
    delivery_mode = models.CharField(blank=True, null=True, max_length=50, verbose_name="Mode de livraison")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité")



class ClientCustomizationForDecoupeLaser(models.Model):

    SUPPORTS = [("T-shirt", "T-shirt"),
                ("Laoste", "Laoste"),
                ("Casquette", "Casquette"),
                ("Polo", "Polo"),
                ("Sweat a capuche", "Sweat a capuche"),
                ("Serviette", "Serviette"),
                ("Sac", "Sac"),
                ("Autre (précisez)", "Autre (précisez)")]

    support_type = models.CharField(blank=True, null=True, choices=SUPPORTS, verbose_name='Type de support',
                                    max_length=30)
    dim_1 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 2')
    quantity = models.IntegerField(verbose_name='Quantité', blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    other_support = models.CharField(blank=True, null=True, verbose_name='Type de support(Personnalisé)', max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class ClientCustomizationForImpression3D(models.Model):

    SUPPORTS = [("T-shirt", "T-shirt"),
                ("Laoste", "Laoste"),
                ("Casquette", "Casquette"),
                ("Polo", "Polo"),
                ("Sweat a capuche", "Sweat a capuche"),
                ("Serviette", "Serviette"),
                ("Sac", "Sac"),
                ("Autre (précisez)", "Autre (précisez)")]

    support_type = models.CharField(blank=True, null=True, choices=SUPPORTS, verbose_name='Type de support',
                                    max_length=30)
    dim_1 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 2')
    quantity = models.IntegerField(verbose_name='Quantité', blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    other_support = models.CharField(blank=True, null=True, verbose_name='Type de support(Personnalisé)', max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class ClientCustomizationForImprPapierEtSupportRigide(models.Model):

    SUPPORTS = [("T-shirt", "T-shirt"),
                ("Laoste", "Laoste"),
                ("Casquette", "Casquette"),
                ("Polo", "Polo"),
                ("Sweat a capuche", "Sweat a capuche"),
                ("Serviette", "Serviette"),
                ("Sac", "Sac"),
                ("Autre (précisez)", "Autre (précisez)")]

    support_type = models.CharField(blank=True, null=True, choices=SUPPORTS, verbose_name='Type de support',
                                    max_length=30)
    dim_1 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 2')
    quantity = models.IntegerField(verbose_name='Quantité', blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    other_support = models.CharField(blank=True, null=True, verbose_name='Type de support(Personnalisé)', max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class ClientCustomizationForTextileEtVetements(models.Model):

    SUPPORTS = [("T-shirt", "T-shirt"),
                ("Laoste", "Laoste"),
                ("Casquette", "Casquette"),
                ("Polo", "Polo"),
                ("Sweat a capuche", "Sweat a capuche"),
                ("Serviette", "Serviette"),
                ("Sac", "Sac"),
                ("Autre (précisez)", "Autre (précisez)")]

    support_type = models.CharField(blank=True, null=True, choices=SUPPORTS, verbose_name='Type de support',
                                    max_length=30)
    dim_1 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 2')
    quantity = models.IntegerField(verbose_name='Quantité', blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    other_support = models.CharField(blank=True, null=True, verbose_name='Type de support(Personnalisé)', max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class ClientCustomizationForImpressSurObjetsPersonnalise(models.Model):

    SUPPORTS = [("T-shirt", "T-shirt"),
                ("Laoste", "Laoste"),
                ("Casquette", "Casquette"),
                ("Polo", "Polo"),
                ("Sweat a capuche", "Sweat a capuche"),
                ("Serviette", "Serviette"),
                ("Sac", "Sac"),
                ("Autre (précisez)", "Autre (précisez)")]

    support_type = models.CharField(blank=True, null=True, choices=SUPPORTS, verbose_name='Type de support',
                                    max_length=30)
    dim_1 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name='Dimension 2')
    quantity = models.IntegerField(verbose_name='Quantité', blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    other_support = models.CharField(blank=True, null=True, verbose_name='Type de support(Personnalisé)', max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
"""
