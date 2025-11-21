from django.contrib import admin
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

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse('service', kwargs={'slug':self.slug})

    @property
    def get_support_field_name(self):
        for field in self.html_fields.all():
            if field.is_support_field:
                return field.get_input_name


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

    def __str__(self):
        return "Commande no {} de {} pour le service {}".format(self.pk, self.user, self.service)

    @property
    @admin.display(description='Numéro de commande')
    def get_id(self):
        return self.id

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

class FieldForService(models.Model):
    
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
        return False
