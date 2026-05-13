from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from Users.models import Fab_User

class ServiceInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom du service', null=False, blank=False)
    description_accueil = models.TextField(verbose_name='Description accueil', default='Pas de description sur accueil', help_text="Cette description s'affichera sur la page d'acueil")
    description = models.TextField(verbose_name='Description', default='Pas de description')
    slug = models.SlugField(default='', blank=True, null=False, max_length=128, verbose_name='Slug')
    impressionNumerique = models.BooleanField(default=False, verbose_name='Service d\'impression numérique ?')
    class_icon_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='class de l\'icône', default='', help_text="Classe de l'icône du service (ex: fa-solid fa-tshirt)")

    def save(self, *args, **kwargs):
        if not self.pk:  # seulement à la création
            if ServiceInfo.objects.count() >= 7:
                raise ValidationError("Maximum de 7 instances atteint.")
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.pk and ServiceInfo.objects.count() >= 7:
            raise ValidationError("Maximum de 7 instances atteint.")

    def __str__(self):
        return self.name
    
    @property
    def get_absolute_url(self):
        return reverse('service', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['name']

class CustomService(models.Model):

    DELIVERIES = [('Retrait sur place (Dakar)','Retrait sur place (Dakar)'),
                  ('Livraison à domicile (Dakar)','Livraison à domicile (Dakar)'),
                  ('Livraison à domicile (Autres régions)','Livraison à domicile (Autres régions)')]

    img_path = models.CharField(max_length=255, verbose_name='Chemin de l\'image', null=True, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    comment = models.TextField(verbose_name='Instructions Spéciales', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Quantité', null=False, blank=False)
    width = models.IntegerField(verbose_name='Largeur (en cm)', null=False, blank=False)
    height = models.IntegerField(verbose_name='Hauteur (en cm)', null=False, blank=False)

    client_name = models.CharField(max_length=100, verbose_name='Nom du client', null=False, blank=True)
    client_email = models.EmailField(verbose_name='Email du client', null=False, blank=True)
    client_phone = models.CharField(max_length=15, verbose_name='Téléphone du client', null=False, blank=True)
    client_address = models.CharField(max_length=255, verbose_name='Adresse du client', null=False, blank=True)
    delivery_mode = models.CharField(max_length=180, verbose_name='Mode de livraison', choices=DELIVERIES, blank=True, null=False)
    
    class Meta:
        abstract = True
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['name']

    def __str__(self):
        return 'Commande pour ' + self.client_name
    
    def get_img_path(self):
        return self.img_path
    
    @property
    def get_absolute_url(self):
        return reverse('service', kwargs={'slug':self.slug})

class ServicesWithColors(CustomService):

    class Meta:
        abstract = False

class Colors(models.Model):

    COLOR_PALETTE = [
        ('#000000', "black", ),
        ("#FF0000", "red", ),
        ("#0000FF", "blue", ),
        ("#FFFFFF", "white"),
        ("#FFC0CB", "pink"),
        ("#5E35B1", "purple"),
        ("#32CD32", "green"),
        ("#FFA500", "orange"),
        ("#FFD700", "yellow"),
        ("#C0C0C0", "silver"),
    ]

    color = ColorField(verbose_name='Couleur', choices=COLOR_PALETTE)
    service = models.ForeignKey(ServicesWithColors, on_delete=models.CASCADE, related_name='selected_colors')

    def __str__(self):
        return f'Couleur {self.color} pour Service {self.service}'

    class Meta:
        verbose_name = 'Couleur pour Service'
        verbose_name_plural = 'Couleurs pour Service'

class GalerieImageForService(models.Model):
    service = models.ForeignKey(ServiceInfo, max_length=60, verbose_name='Service', null=True, blank=True, related_name='galerie_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Services/galerie_image', default='Services/galerie_image/default3.png',verbose_name='Image')

    def __str__(self):
        return f'Image no {self.pk} du service {self.service}'
    
    class Meta:
        verbose_name = "Image de la galerie pour service"
        verbose_name_plural = "Images de la galerie pour services"

class BroderieNumeriqueModel(ServicesWithColors):

    SUPPORTS = [
        ("T-shirt","T-shirt"),
        ("Casquette","Casquette"),
        ("Laoste","Laoste"),
        ("Polo","Polo"),
        ("Sweat à capuche","Sweat à capuche"),
        ("Serviette","Serviette"),
        ("Sac","Sac"),
        ("Autre (Préciser)","Autre (Préciser)"),
        ]

    image = models.ImageField(upload_to='Services/BroderieNumerique', verbose_name='Image à broder', null=False, blank=True,)
    support_type = models.CharField(max_length=100, verbose_name='Type de support', choices=SUPPORTS, null=False, blank=False)
    other_support = models.CharField(max_length=100, verbose_name='Autre support (si applicable)', null=True, blank=True)

    def __str__(self):
        return f'Broderie Numérique No {self.pk} - Support: {self.support_type} - Taille: {self.width}x{self.height} cm - Quantité: {self.quantity}'

    def get_obj(self):
        if self.support_type=="Autre (Préciser)":
            return self.other_support
        return self.support_type
    
    def get_img_path(self):
        try:
            return self.image.url
        except ValueError:
            return super().get_img_path()



    class Meta:
        verbose_name = 'Commande pour broderie Numérique'
        verbose_name_plural = 'Commandes pour broderie Numérique'

class FraiseCNCModel(CustomService):

    SERVICES = [
        ("Découpe","Découpe"),
        ("Gravure","Gravure"),
        ]
    
    MATERIALS = [
        ("Bois","Bois"),
        ("Aluminium","Aluminium"),
        ("PVC","PVC"),
        ]

    image = models.ImageField(upload_to='Services/FraiseCNC', verbose_name='Image à fraiser', null=False, blank=True)
    service_type = models.CharField(max_length=100, verbose_name='Type de service', choices=SERVICES, null=False, blank=False)
    used_material = models.CharField(max_length=100, verbose_name='Matériau utilisé', choices=MATERIALS, null=False, blank=False)

    def __str__(self):
        return f'Fraise CNC No {self.pk} - Matériau: {self.used_material} - Taille: {self.width}x{self.height} cm - Quantité: {self.quantity}'

    def get_obj(self):
        return self.service_type + ' sur ' + self.used_material

    def get_img_path(self):
        try:
            return self.image.url
        except ValueError:
            return super().get_img_path()

    class Meta:
        verbose_name = 'Commande pour Fraise CNC'
        verbose_name_plural = 'Commandes pour Fraise CNC'

class DecoupeLaserModel(CustomService):

    SERVICES = [
        ("Découpe","Découpe"),
        ("Gravure","Gravure"),]

    MATERIALS = [
        ("Bois","Bois"),
        ("Acrylic","Acrylic"),
        ("Cuir","Cuir"),
        ("Métal","Métal"),
        ]

    image = models.ImageField(upload_to='Services/DecoupeLaser', verbose_name='Image à découper', null=False, blank=True)
    service_type = models.CharField(max_length=100, verbose_name='Type de service', choices=SERVICES, null=False, blank=False)
    used_material = models.CharField(max_length=100, verbose_name='Matériau utilisé', choices=MATERIALS, null=False, blank=False)

    def __str__(self):
        return f'Découpe Laser No {self.pk} - Matériau: {self.used_material} - Taille: {self.width}x{self.height} cm - Quantité: {self.quantity}'
    
    def get_obj(self):
        return self.service_type + ' sur ' + self.used_material

    def get_img_path(self):
        try:
            return self.image.url
        except ValueError:
            return super().get_img_path()

    class Meta:
        verbose_name = 'Commande pour Découpe Laser'
        verbose_name_plural = 'Commandes pour Découpe Laser'

class Impression3DModel(ServicesWithColors):

    IMPRESSIONS = [
        ("PLA(Plastique)","PLA(Plastique)"),
        ("SLA(Résine)","SLA(Résine)"),
        ("SLS(Poudre)","SLS(Poudre)"),
        ]

    MATERIALS = [
        ("PLA","PLA"),
        ("ABS","ABS"),
        ("PETG","PETG"),
        ("RESINE","RESINE"),
        ]

    image = models.ImageField(upload_to='Services/Impression3D', verbose_name='Image à imprimer', null=False, blank=True)
    impression_type = models.CharField(max_length=100, verbose_name='Type d\'impression', choices=IMPRESSIONS, null=False, blank=False)
    used_material = models.CharField(max_length=100, verbose_name='Matériau utilisé', choices=MATERIALS, null=False, blank=False)

    def __str__(self):
        return f'Impression 3D No {self.pk} - Matériau: {self.material_type} - Taille: {self.width}x{self.height}x{self.depth} cm - Quantité: {self.quantity}'
    
    def get_obj(self):
        return self.impression_type + ' sur ' + self.used_material

    def get_img_path(self):
        try:
            return self.image.url
        except ValueError:
            return super().get_img_path()

    class Meta:
        verbose_name = 'Commande pour Impression 3D'
        verbose_name_plural = 'Commandes pour Impression 3D'

class ImpressionPaperSupportRigideModel(ServicesWithColors):

    FORMATS = [
        ("A3","A3"),
        ("A4","A4"),
        ("A5","A5"),
        ("Autre (Préciser)","Autre (Préciser)"),
    ]

    PAPERS = [
        ("mat","mat"),
        ("brillant","brillant"),
        ("recyclé","recyclé"),
        ("Autre (Préciser)","Autre (Préciser)"),
        ]

    DESIGN_FILES = [
        ("PNG","PNG"),
        ("AI","AI"),
        ("PSD","PSD"),
        ("Autre (Préciser)","Autre (Préciser)"),
        ]

    image = models.ImageField(upload_to='Services/ImpressionPaperSupportRigide', verbose_name='Image à imprimer', null=False, blank=True)
    format = models.CharField(max_length=100, verbose_name='Format souhaité', choices=FORMATS, null=False, blank=False)
    other_format = models.CharField(max_length=100, verbose_name='Autre format (si applicable)', null=True, blank=True)
    paper_type = models.CharField(max_length=100, verbose_name='Type de papier', choices=PAPERS, null=False, blank=False)
    other_paper = models.CharField(max_length=100, verbose_name='Autre papier (si applicable)', null=True, blank=True)
    design_file = models.CharField(max_length=50, choices=DESIGN_FILES, verbose_name='Fichier de design', null=False, blank=False)
    other_file = models.CharField(max_length=100, verbose_name='Autre fichier (si applicable)', null=True, blank=True)

    def __str__(self):
        return f'Impression Papier/Support Rigide No {self.pk} - Format: {self.format} - Taille: {self.width}x{self.height} cm - Quantité: {self.quantity}'
    
    def get_obj(self):
        if self.paper_type=="Autre (Préciser)":
            if self.format=="Autre (Préciser)":
                return 'Papier ' + self.other_paper + ' format ' + self.other_format
            return 'Papier ' + self.other_paper + ' format ' + self.format
        return 'Papier ' + self.paper_type + ' format ' + self.format

    def get_img_path(self):
        try:
            return self.image.url
        except ValueError:
            return super().get_img_path()


    class Meta:
        verbose_name = 'Commande pour Impression Papier/Support Rigide'
        verbose_name_plural = 'Commandes pour Impression Papier/Support Rigide'

class ImpressionTextileEtVetementModel(ServicesWithColors):

    TEXTILES = [
        ("Coton","Coton"),
        ("Polyester","Polyester"),
        ("Autre (Préciser)","Autre (Préciser)"),
    ]

    IMPRESSIONS = [
        ("Sérigraphie","Sérigraphie"),
        ("Sublimation","Sublimation"),
        ("Impression","Impression"),
        ("Direct", "Direct"),
    ]

    DESIGN_FILES = [
        ("PNG","PNG"),
        ("AI","AI"),
        ("PSD","PSD"),
        ("Autre (Préciser)","Autre (Préciser)"),
    ]


    image = models.ImageField(upload_to='Services/ImpressionTextileEtVetement', verbose_name='Image à imprimer', null=False, blank=True)
    textile_type = models.CharField(max_length=100, verbose_name='Type de textile', choices=TEXTILES, null=False, blank=False)
    other_textile = models.CharField(max_length=100, verbose_name='Autre textile (si applicable)', null=True, blank=True)
    impression_type = models.CharField(max_length=100, verbose_name='Type d\'impression', choices=IMPRESSIONS, null=False, blank=False)
    design_file = models.CharField(max_length=50, choices=DESIGN_FILES, verbose_name='Fichier de design', null=False, blank=False)
    other_design_file = models.CharField(max_length=100, verbose_name='Autre fichier (si applicable)', null=True, blank=True)

    def __str__(self):
        return f'Impression Textile et Vêtement No {self.pk} - Textile: {self.textile_type} - Taille: {self.size} - Couleur: {self.color} - Quantité: {self.quantity}'
    
    def get_obj(self):
        if self.textile_type=="Autre (Préciser)":
            return self.other_textile + ' impression ' + self.impression_type
        return self.textile_type + ' impression ' + self.impression_type

    def get_img_path(self):
        try:
            return self.image.url
        except ValueError:
            return super().get_img_path()

    class Meta:
        verbose_name = 'Commande pour Impression Textile et Vêtement'
        verbose_name_plural = 'Commandes pour Impression Textile et Vêtement'

class ImpressionObjPersonnaliseModel(ServicesWithColors):

    OBJECTS = [
        ("T-shirt","T-shirt"),
        ("Casquette","Casquette"),
        ("Laoste","Laoste"),
        ("Polo","Polo"),
        ("Sweat à capuche","Sweat à capuche"),
        ("Serviette","Serviette"),
        ("Sac","Sac"),
        ("Autre (Préciser)","Autre (Préciser)"),
        ]
    
    DESIGN_FILES = [
        ("PNG","PNG"),
        ("AI","AI"),
        ("PSD","PSD"),
        ("Autre (Préciser)","Autre (Préciser)"),
                    ]

    image = models.ImageField(upload_to='Services/ImpressionObjPersonnalise', verbose_name='Image à imprimer', null=False, blank=True)
    obj_type = models.CharField(max_length=100, verbose_name='Type d\'objet', choices=OBJECTS, null=False, blank=False)
    other_object = models.CharField(max_length=100, verbose_name='Autre objet (si applicable)', null=True, blank=True)
    design_file = models.CharField(max_length=50, choices=DESIGN_FILES, verbose_name='Fichier de design', null=False, blank=False)
    other_file = models.CharField(max_length=100, verbose_name='Autre fichier (si applicable)', null=True, blank=True)

    def __str__(self):
        return f'Impression Objet Personnalisé No {self.pk} - Objet: {self.object_type} - Matériau: {self.material} - Quantité: {self.quantity}'
    
    def get_obj(self):
        if self.obj_type=="Autre (Préciser)":
            return self.other_object
        return self.obj_type

    def get_img_path(self):
        try:
            return self.image.url
        except ValueError:
            return super().get_img_path()


    class Meta:
        verbose_name = 'Commande pour Impression Objet Personnalisé'
        verbose_name_plural = 'Commandes pour Impression Objet Personnalisé'

"""# Create your models here.
class Service(models.Model):

    @property
    def get_support_field_name(self):
        for field in self.html_fields.all():
            if field.is_support_field:
                return field.get_input_name"""

    
"""class CustomizedService(models.Model):

    DELIVERIES = [('Retrait sur place (Dakar)','Retrait sur place (Dakar)'),
                  ('Livraison à domicile (Dakar)','Livraison à domicile (Dakar)'),
                  ('Livraison à domicile (Autres régions)','Livraison à domicile (Autres régions)')]

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='custom_services')
    imported_picture = models.ImageField(upload_to='Services/user_imported_imgs', blank=True, null=True ,verbose_name='Image importée')
    chosen_picture = models.URLField(verbose_name='Image choisie', blank=True, null=True)
    adress_delivery = models.CharField(verbose_name='Adresse de livraison', blank=False, null=False)
    delivery_mode = models.CharField(max_length=180, verbose_name='Mode de livraison', blank=False, null=False, choices=DELIVERIES)
    fields_value = models.JSONField(default=dict)
    cgu_accept = models.BooleanField(default=False, verbose_name="Accepter les conditions de confidentialité")
    date = models.DateTimeField(verbose_name='Date de la commande', default=timezone.now)

    def __str__(self):
        return "Commande no {} de {} pour le service {}".format(self.pk, self.user, self.service)

    @property
    @admin.display(description='Numéro de commande')
    def get_id(self):
        return self.id

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = 'Commandes'"""

"""class FieldForService(models.Model):
    
    TYPES = [('Commentaire','Commentaire'),('Entier', 'Entier'),
    ("Liste d'entiers","Liste d'entiers"),
    ("Liste de caractères","Liste de caractères")]


    service = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name='html_fields', null=True)
    html_field = models.TextField(verbose_name='Code Html des Champs', blank=False, null=False, help_text="Si c'est un champ groupé, les names des inputs doivent être différents et être comme [first_nom_champ, last_nom_champ]")
    grouped = models.BooleanField(verbose_name='Champs groupé ?', default=False, help_text="Le champ est-il groupé ? (plusieurs inputs pour un même champ)")
    header_icon_class = models.CharField(max_length=64, null=False, blank=False, verbose_name='class du header', help_text="Classe de l'icône du header (ex: fa-solid fa-user)")
    header_icon_txt = models.CharField(max_length=64, default='', null=False, blank=False, verbose_name='Texte du header', help_text="Texte du header (ex: Instructions spéciales)")
    is_support_field = models.BooleanField(default=False, verbose_name='Champs de support ?')

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
        return False"""

