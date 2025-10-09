from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from Users.models import Fab_User
from .validators import validate_file_size, validate_file_extension1, validate_file_extension3, \
    validate_file_extension2, validate_file_extension4


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=60, verbose_name='Nom', blank=False, null=False)
    description_accueil = models.TextField(verbose_name='Description accueil', default='Pas de description sur accueil', help_text="Cette description s'affichera sur la page d'acueil")
    description = models.TextField(verbose_name='Description', default='Pas de description')
    slug = models.SlugField(default='', blank=True, null=False, max_length=128, verbose_name='Slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse('service', kwargs={'slug':self.slug})

class GalerieImageForService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, verbose_name='Service', related_name='galerie_images', null=True)
    image = models.ImageField(upload_to='Services/galerie_image', default='Services/galerie_image/default3.png',
                              verbose_name='Image')

    def __str__(self):
        return f'Image no {self.pk} du service {self.service} '
    
    class Meta:
        verbose_name = "Image de la galerie pour service"
        verbose_name_plural = "Images de la galerie pour services"
    
class CustomizedService(models.Model):

    DELIVERIES = [('Retrait sur place (Dakar)','Retrait sur place (Dakar)'),
                  ('Livraison à domicile (Dakar)','Livraison à domicile (Dakar)'),
                  ('Livraison à domicile (Autres régions)','Livraison à domicile (Autres régions)')]

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='custom_services')
    imported_picture = models.ImageField(upload_to='Services/user_imported_imgs', blank=True, null=True ,verbose_name='Image importée')
    chosen_picture = models.URLField(verbose_name='Image choisie', blank=True, null=True)
    adress_delivery = models.CharField(verbose_name='Adresse de livraison', blank=False, null=False, choices=DELIVERIES)
    delivery_mode = models.CharField(max_length=180, verbose_name='Mode de livraison', blank=False, null=False)
    fields_value = models.JSONField(default=dict)
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité")
    date = models.DateTimeField(verbose_name='Date de la commande', default=timezone.now)

class FieldForService(models.Model):
    
    TYPES = [('Commentaire','Commentaire'),('Entier', 'Entier'),
    ("Liste d'entiers","Liste d'entiers"),
    ("Liste de caractères","Liste de caractères")]


    service = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name='html_fields', null=True)
    html_field = models.TextField(verbose_name='Code Html des Champs', blank=False, null=False, help_text="Si c'est un champ groupé, les names des inputs doivent être différents et être comme [first_nom_champ, last_nom_champ]")
    grouped = models.BooleanField(verbose_name='Champs groupé ?', default=False, help_text="Le champ est-il groupé ? (plusieurs inputs pour un même champ)")
    header_icon_class = models.CharField(max_length=64, null=False, blank=False, verbose_name='class du header', help_text="Classe de l'icône du header (ex: fa-solid fa-user)")
    header_icon_txt = models.CharField(max_length=64, default='', null=False, blank=False, verbose_name='Texte du header', help_text="Texte du header (ex: Instructions spéciales)")

    def __str__(self):
        return f'Champ No {self.pk} du service {self.service}'

    class Meta:
        verbose_name = "Champ pour service personnalisé"
        verbose_name_plural = "Champs pour services personnalisés"

    @property
    def get_input_name(self):
        '''
        returns the name of the input
        '''
        import re
        if not self.grouped:
            # if there is only one field or input in self.html_field
            pattern = r'name=["\'](.*?)["\']'
            matches = re.findall(pattern, self.html_field)
            if len(matches)>1:
                return matches
            elif len(matches)==1:
                return matches[0]
            else:
                return None
        else:
            # if there is more than 1 field or input, then create a regex that returns all the names of these fields or inputs
            # when the field is grouped, the names of the inputs must be different and be like [first_nom_champ, last_nom_champ]
            pattern = r'name=["\'](.*?)["\']'
            matches = re.findall(pattern, self.html_field)
            return matches
        
    def is_color_field(self):
        '''
        returns True if in self.html_field there is an input with name="selected-colors", False otherwise.
        '''

        import re
        pattern = r'name=["\']selected-colors["\']'
        matches = re.findall(pattern, self.html_field)
        if matches:
            return True
        return False

"""        
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

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, verbose_name='Service')

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

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL)

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

    service = models.ForeignKey(Service, on_delete=models.SET_NULL)

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

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL)

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

    service = models.ForeignKey(Service, on_delete=models.SET_NULL)

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

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL)

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

    service = models.ForeignKey(Service, on_delete=models.SET_NULL)

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

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL)

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

    service = models.ForeignKey(Service, on_delete=models.SET_NULL)

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

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL)

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

    service = models.ForeignKey(Service, on_delete=models.SET_NULL)

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

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL)

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

    service = models.ForeignKey(Service, on_delete=models.SET_NULL)

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

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL)

    town = models.CharField(max_length=60, verbose_name="Adresse (ville)", blank=False, null=False)
    delivery_mode = models.CharField(max_length=50, choices=LIVRAISON,
                                     verbose_name="Mode de livraison", blank=False, null=False, default="Retrait sur place Dakar")
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité", blank=False, null=False)
"""