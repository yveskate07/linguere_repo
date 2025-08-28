from django.db import models
from Users.models import Fab_User
from .validators import validate_file_size, validate_file_extension1, validate_file_extension3, \
    validate_file_extension2, validate_file_extension4


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=60, verbose_name='Nom', blank=False, null=False)
    description = models.TextField(verbose_name='Description')
    image1 = models.ImageField(upload_to='Services/service_image', default='Services/service_image/default3.png',
                               verbose_name='Image 1')
    image2 = models.ImageField(upload_to='Services/service_image', default='Services/service_image/default3.png',
                               verbose_name='Image 2')
    image3 = models.ImageField(upload_to='Services/service_image', default='Services/service_image/default3.png',
                               verbose_name='Image 3')
    image4 = models.ImageField(upload_to='Services/service_image', default='Services/service_image/default3.png',
                               verbose_name='Image 4')
    image5 = models.ImageField(upload_to='Services/service_image', default='Services/service_image/default3.png',
                               verbose_name='Image 5')
    image6 = models.ImageField(upload_to='Services/service_image', default='Services/service_image/default3.png',
                               verbose_name='Image 6')
    image7 = models.ImageField(upload_to='Services/service_image', default='Services/service_image/default3.png',
                               verbose_name='Image 7')
    image8 = models.ImageField(upload_to='Services/service_image', default='Services/service_image/default3.png',
                               verbose_name='Image 8')

    def __str__(self):
        return self.name


class ClientCustomizationForBroderieNumerique(models.Model):
    SUPPORTS = [("T-shirt", "T-shirt"),
                ("Casquette", "Casquette"),
                ("Laoste", "Laoste"),
                ("Polo", "Polo"),
                ("Sweat à capuche", "Sweat à capuche"),
                ("Serviette", "Serviette"),
                ("Sac", "Sac"),
                ("Autre (précisez)", "Autre (précisez)")]

    LIVRAISON = [("Retrait sur place Dakar", "Retrait sur place Dakar"),
                 ("Livraison à domicile (Dakar)", "Livraison à domicile (Dakar)"),
                 ("Livraison à domicile (Autres régions)", "Livraison à domicile (Autres régions)")]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Service')

    support_type = models.CharField(choices=SUPPORTS, verbose_name='Type de support', max_length=30, default='T-shirt', blank=False, null=False)
    other_support = models.TextField(blank=True, null=True, verbose_name='Support personnalisé')
    date = models.DateTimeField(auto_now_add=True)
    dim_1 = models.IntegerField(verbose_name='Dimension 1', blank=False, null=False)
    dim_2 = models.IntegerField(verbose_name='Dimension 2', blank=False, null=False)
    quantity = models.IntegerField(verbose_name='Quantité', blank=False, null=False)
    special_instructions = models.TextField(verbose_name='Instructions', blank=False, null=False)
    design_picture = models.CharField(verbose_name="Image du design", blank=True, null=True, max_length=260)
    upload_design_picture = models.ImageField(verbose_name="Design uploadé", upload_to="Services/uploaded_design",
                                              blank=True, null=True,
                                              validators=[validate_file_size, validate_file_extension1])
    codeCouleur = models.CharField(max_length=80, verbose_name='Code couleur', blank=True, null=True)

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)

    town = models.CharField(max_length=60, verbose_name="Adresse (ville)", blank=False, null=False)
    delivery_mode = models.CharField(max_length=50, choices=LIVRAISON, verbose_name="Mode de livraison", blank=False, null=False, default="Retrait sur place Dakar")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité", blank=False, null=False)

    class Meta:
        verbose_name = "Commandes pour services Broderie"

    def __str__(self):
        return self.name


class ClientCustomizationForFraiseuseNumerique(models.Model):
    LIVRAISONS = [("Retrait sur place Dakar", "Retrait sur place Dakar"),
                  ("Livraison à domicile (Dakar)", "Livraison à domicile (Dakar)"),
                  ("Livraison à domicile (Autres régions)", "Livraison à domicile (Autres régions)")]

    SERVICES = [("Découpe", "Découpe"),
                ("Gravure", "Gravure"), ]

    MATERIALS = [("Bois", "Bois"),
                 ("Aluminium", "Aluminium"),
                 ("PVC", "PVC"), ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    service_type = models.CharField(choices=SERVICES, verbose_name='Type de service', max_length=30, default="Découpe", blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    dim_1 = models.CharField(max_length=30, verbose_name='Dimension 1', blank=False, null=False)
    dim_2 = models.CharField(max_length=30, verbose_name='Dimension 2', blank=False, null=False)
    used_materials = models.CharField(choices=MATERIALS, max_length=30, verbose_name='Matériau utilisé', default="Bois", blank=False, null=False)
    quantity = models.IntegerField(verbose_name='Quantité', blank=False, null=False)
    special_instructions = models.TextField(blank=False, null=False)
    design_picture = models.CharField(verbose_name="Image du design", blank=True, null=True, max_length=260)
    upload_design_picture = models.ImageField(verbose_name="Design uploadé", upload_to="Services/uploaded_design",
                                              blank=True, null=True,
                                              validators=[validate_file_size, validate_file_extension1])

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)

    town = models.CharField(max_length=60, verbose_name="Adresse (ville)")
    delivery_mode = models.CharField(max_length=50, choices=LIVRAISONS, verbose_name="Mode de livraison", default="Retrait sur place Dakar")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité")


class ClientCustomizationForDecoupeLaser(models.Model):
    SERVICES = [("Découpe", "Découpe"),
                ("Gravure", "Gravure"), ]

    MATERIALS = [("Acrylique", "Acrylique"),
                 ("Bois", "Bois"),
                 ("Métal", "Métal"),
                 ("Cuir", "Cuir"), ]

    LIVRAISON = [("Retrait sur place Dakar", "Retrait sur place Dakar"),
                 ("Livraison à domicile (Dakar)", "Livraison à domicile (Dakar)"),
                 ("Livraison à domicile (Autres régions)", "Livraison à domicile (Autres régions)")]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    service_type = models.CharField(blank=False, null=False, choices=SERVICES, verbose_name='Type de service',
                                    max_length=30, default="Découpe")
    date = models.DateTimeField(auto_now_add=True)
    dim_1 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 2')
    used_materials = models.CharField(blank=False, null=False, max_length=30, choices=MATERIALS,
                                      verbose_name='Matériau utilisé', default="Acrylique")
    quantity = models.IntegerField(verbose_name='Quantité', blank=False, null=False)
    special_instructions = models.TextField(blank=False, null=False)
    design_picture = models.CharField(verbose_name="Image du design", blank=True, null=True, max_length=260)
    upload_design_picture = models.ImageField(verbose_name="Design uploadé", upload_to="Services/uploaded_design",
                                              blank=True, null=True,
                                              validators=[validate_file_size, validate_file_extension3])

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)

    town = models.CharField(max_length=60, verbose_name="Adresse (ville)", blank=False, null=False)
    delivery_mode = models.CharField(max_length=50, choices=LIVRAISON,
                                     verbose_name="Mode de livraison", blank=False, null=False, default="Retrait sur place Dakar")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité", blank=False, null=False)


class ClientCustomizationForImpression3D(models.Model):
    LIVRAISON = [("Retrait sur place Dakar", "Retrait sur place Dakar"),
                 ("Livraison à domicile (Dakar)", "Livraison à domicile (Dakar)"),
                 ("Livraison à domicile (Autres régions)", "Livraison à domicile (Autres régions)")]

    MATERIALS = [("PLA", "PLA"),
                 ("ABS", "ABS"),
                 ("PETG", "PETG"),
                 ("Résine", "Résine"), ]

    IMPRESSIONS = [("FDM(Plastique)", "FDM(Plastique)"),
                   ("SLA(Résine)", "SLA(Résine)"),
                   ("SLS(Poudre)", "SLS(Poudre)"), ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    impression_type = models.CharField(choices=IMPRESSIONS, verbose_name="Type d'impression",
                                       max_length=30, default="FDM(Plastique)", blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    dim_1 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 2')
    codeCouleur = models.CharField(max_length=80, blank=False, null=False, verbose_name='Code couleur')
    used_materials = models.CharField(choices=MATERIALS, max_length=30, verbose_name='Matériau utilisé', default="PLA", blank=False, null=False)
    quantity = models.IntegerField(verbose_name='Quantité', blank=False, null=False)
    special_instructions = models.TextField(blank=False, null=False)

    design_picture = models.CharField(verbose_name="Image du design", blank=True, null=True, max_length=260)
    upload_design_picture = models.ImageField(verbose_name="Design uploadé", upload_to="Services/uploaded_design",
                                              blank=True, null=True,
                                              validators=[validate_file_size, validate_file_extension4])

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)

    town = models.CharField(blank=False, null=False, max_length=60, verbose_name="Adresse (ville)")
    delivery_mode = models.CharField(blank=False, null=False, max_length=50, choices=LIVRAISON,
                                     verbose_name="Mode de livraison", default="Retrait sur place Dakar")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité", blank=False, null=False)


class ClientCustomizationForPaper(models.Model):
    LIVRAISON = [("Retrait sur place Dakar", "Retrait sur place Dakar"),
                 ("Livraison à domicile (Dakar)", "Livraison à domicile (Dakar)"),
                 ("Livraison à domicile (Autres régions)", "Livraison à domicile (Autres régions)")]

    FORMATS = [("A4", "A4"),
               ("A3", "A3"),
               ("A5", "A5"),
               ("Autre (précisez)", "Autre (précisez)")]

    PAPERS = [("Mat", "Mat"),
              ("Brillant", "Brillant"),
              ("Recyclé", "Recyclé"),
              ("Autre (précisez)", "Autre (précisez)")]

    DESIGNS_FILE = [("AI", "AI"),
                    ("PNG", "PNG"),
                    ("PSD", "PSD"),
                    ("Autre (précisez)", "Autre (précisez)")]

    wished_format = models.CharField(choices=FORMATS, verbose_name='Format souhaité', max_length=30, default="A4", blank=False, null=False)
    other_format = models.CharField(max_length=60, blank=True, null=True, verbose_name='Autre format')
    paper = models.CharField(choices=PAPERS, verbose_name='Type de papier', max_length=60, default="Mat", blank=False, null=False)

    other_paper = models.CharField(max_length=60, blank=True, null=True, verbose_name='Autre papier')

    design_file = models.CharField(choices=DESIGNS_FILE, max_length=30, verbose_name='Fichier du design', default="AI", blank=False, null=False)

    other_design_file = models.CharField(max_length=60, blank=True, null=True, verbose_name='Autre fichier de design')

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)
    dim_1 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 2')
    codeCouleur = models.CharField(max_length=80, blank=False, null=False, verbose_name='Code couleur')
    quantity = models.IntegerField(verbose_name='Quantité', blank=False, null=False)
    special_instructions = models.TextField(blank=False, null=False)
    design_picture = models.CharField(verbose_name="Image du design", blank=True, null=True, max_length=260)
    upload_design_picture = models.ImageField(verbose_name="Design uploadé", upload_to="Services/uploaded_design",
                                              blank=True, null=True,
                                              validators=[validate_file_size, validate_file_extension4])

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)

    town = models.CharField(max_length=60, verbose_name="Adresse (ville)", blank=False, null=False)
    delivery_mode = models.CharField(max_length=50, choices=LIVRAISON,
                                     verbose_name="Mode de livraison", blank=False, null=False, default="Retrait sur place Dakar")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité", blank=False, null=False)


class ClientCustomizationForTextile(models.Model):
    LIVRAISON = [("Retrait sur place Dakar", "Retrait sur place Dakar"),
                 ("Livraison à domicile (Dakar)", "Livraison à domicile (Dakar)"),
                 ("Livraison à domicile (Autres régions)", "Livraison à domicile (Autres régions)")]

    TEXTILES = [("Coton", "Coton"),
                ("Polyester", "Polyester"),
                ("Autre (précisez)", "Autre (précisez)")]

    IMPRESSIONS = [("Serigraphie", "Sérigraphie"),
                   ("Impression", "Impression"),
                   ("Sublimation", "Sublimation"),
                   ("Directe", "Directe")]

    DESIGNS_FILE = [("AI", "AI"),
                    ("PNG", "PNG"),
                    ("PSD", "PSD"),
                    ("Autre (précisez)", "Autre (précisez)")]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    textile_type = models.CharField(choices=TEXTILES, verbose_name='Type de textile', max_length=30, default="Coton", blank=False, null=False)
    other_textile = models.CharField(max_length=60, blank=True, null=True, verbose_name='Autre textile')
    impression_wished = models.CharField(choices=IMPRESSIONS, verbose_name="Type d'impression souhaité",
                                         max_length=60, default="Serigraphie", blank=False, null=False)

    design_file = models.CharField(choices=DESIGNS_FILE, max_length=30, verbose_name='Fichier du design', default="AI", blank=False, null=False)
    other_design_file = models.CharField(max_length=60, blank=True, null=True, verbose_name='Autre fichier de design')

    date = models.DateTimeField(auto_now_add=True)
    dim_1 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 2')
    codeCouleur = models.CharField(max_length=80, blank=False, null=False, verbose_name='Code couleur')
    quantity = models.IntegerField(verbose_name='Quantité', blank=False, null=False)
    special_instructions = models.TextField(blank=False, null=False)
    design_picture = models.CharField(verbose_name="Image du design", blank=True, null=True, max_length=260)
    upload_design_picture = models.ImageField(verbose_name="Design uploadé", upload_to="Services/uploaded_design",
                                              blank=True, null=True,
                                              validators=[validate_file_size, validate_file_extension4])

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)

    town = models.CharField(max_length=60, verbose_name="Adresse (ville)", blank=False, null=False)
    delivery_mode = models.CharField(max_length=50, choices=LIVRAISON,
                                     verbose_name="Mode de livraison", blank=False, null=False, default="Retrait sur place Dakar")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité", blank=False, null=False)


class ClientCustomizationForObjects(models.Model):
    LIVRAISON = [("Retrait sur place Dakar", "Retrait sur place Dakar"),
                 ("Livraison à domicile (Dakar)", "Livraison à domicile (Dakar)"),
                 ("Livraison à domicile (Autres régions)", "Livraison à domicile (Autres régions)")]

    OBJECTS = [("T-shirt", "T-shirt"),
               ("Casquette", "Casquette"),
               ("Laoste", "Laoste"),
               ("Polo", "Polo"),
               ("Sweat à capuche", "Sweat à capuche"),
               ("Serviette", "Serviette"),
               ("Sac", "Sac"),
               ("Autre (précisez)", "Autre (précisez)")]

    DESIGNS_FILE = [("AI", "AI"),
                    ("PNG", "PNG"),
                    ("PSD", "PSD"),
                    ("Autre (précisez)", "Autre (précisez)")]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    object = models.CharField(choices=OBJECTS, verbose_name="Type de d'objet", max_length=30, default="T-shirt", blank=False, null=False)

    other_object = models.CharField(max_length=60, blank=True, null=True, verbose_name='Autre objet')

    design_file = models.CharField(choices=DESIGNS_FILE, max_length=30, verbose_name='Fichier du design', default="AI", blank=False, null=False)

    other_design_file = models.CharField(max_length=60, blank=True, null=True, verbose_name='Autre fichier de design')

    date = models.DateTimeField(auto_now_add=True)
    dim_1 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 1')
    dim_2 = models.CharField(blank=False, null=False, max_length=30, verbose_name='Dimension 2')
    codeCouleur = models.CharField(max_length=80, blank=False, null=False, verbose_name='Code couleur')
    quantity = models.IntegerField(verbose_name='Quantité', blank=False, null=False)
    special_instructions = models.TextField(blank=False, null=False)
    design_picture = models.CharField(verbose_name="Image du design", blank=True, null=True, max_length=260)
    upload_design_picture = models.ImageField(verbose_name="Design uploadé", upload_to="Services/uploaded_design",
                                              blank=True, null=True,
                                              validators=[validate_file_size, validate_file_extension4])

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)

    town = models.CharField(max_length=60, verbose_name="Adresse (ville)", blank=False, null=False)
    delivery_mode = models.CharField(max_length=50, choices=LIVRAISON,
                                     verbose_name="Mode de livraison", blank=False, null=False, default="Retrait sur place Dakar")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité", blank=False, null=False)
