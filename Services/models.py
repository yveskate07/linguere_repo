from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# ==============================================================================
# MODÈLE DE BASE : décrit un service (ex: Broderie Numérique)
# Géré par le client depuis l'admin Django
# ==============================================================================

class Service(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Nom du service',
        null=False, blank=False
    )
    description_accueil = models.TextField(
        verbose_name='Description accueil',
        default='Pas de description sur accueil',
        help_text="Cette description s'affichera sur la page d'accueil"
    )
    description = models.TextField(
        verbose_name='Description',
        default='Pas de description'
    )
    slug = models.SlugField(
        default='', blank=True, null=False,
        max_length=128, verbose_name='Slug'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse('service', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['name']


# ==============================================================================
# MODÈLE DE CHAMP DYNAMIQUE : définit les champs spécifiques à chaque service
# Le client peut ajouter/supprimer des champs depuis l'admin sans toucher au code
# ==============================================================================

class ServiceField(models.Model):

    FIELD_TYPES = [
        ('text',       'Texte libre'),
        ('integer',    'Nombre entier'),
        ('select',     'Liste déroulante (choix unique)'),
        ('multicolor', 'Sélecteur de couleurs (choix multiple)'),
        ('boolean',    'Case à cocher (Oui/Non)'),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='fields',
        verbose_name='Service'
    )
    name = models.SlugField( # has to be in a readonly state, generated from label if not provided, and unique per service
        max_length=100,
        verbose_name='Nom technique',
        null=False, blank=False,
        help_text="Identifiant unique sans espaces ni accents (ex: support_type)",
        editable=False
    )
    label = models.CharField(
        max_length=150,
        verbose_name='Label affiché',
        help_text="Ce que l'utilisateur verra (ex: Type de support)"
    )
    field_type = models.CharField(
        max_length=20,
        choices=FIELD_TYPES,
        verbose_name='Type de champ'
    )
    required = models.BooleanField(
        default=True,
        verbose_name='Obligatoire ?'
    )
    # Pour les champs de type "select" : stocker les options en JSON
    # Exemple : ["T-shirt", "Casquette", "Polo", "Autre (Préciser)"]
    choices = models.JSONField(
        null=True, blank=True,
        verbose_name='Options (pour liste déroulante) / Liste de couleurs (pour multicolor)',
        help_text='Liste des choix au format JSON. Ex: ["Option1", "Option2"]'
    )
    # Si "Autre (Préciser)" est une option, activer ce booléen
    # pour qu'un champ texte libre apparaisse quand l'utilisateur choisit "Autre"
    has_other = models.BooleanField(
        default=False,
        verbose_name='A une option "Autre (Préciser)" ?'
    )
    # Ordre d'affichage dans le formulaire
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )

    class Meta:
        verbose_name = 'Champ de personnalisation'
        verbose_name_plural = 'Champs de personnalisation'
        ordering = ['service', 'order']
        # Un nom technique doit être unique par service
        unique_together = [('service', 'name')]
        

    def __str__(self):
        return f'{self.label} - {self.service.name}'

    def save(self, *args, **kwargs):
        # Validation : si le champ est de type "select", il doit y avoir au moins une option
        if self.field_type == 'select':
            if not self.choices or not isinstance(self.choices, list) or len(self.choices) == 0:
                raise ValidationError('Un champ de type "select" doit avoir au moins une option dans "choices".')
        # Générer un nom technique à partir du label si le nom n'est pas fourni
        self.name = self.label.replace(' ', '_').lower()  # Convertir les espaces en underscores et mettre en minuscules

        super().save(*args, **kwargs)

# ==============================================================================
# MODÈLE DE COMMANDE GÉNÉRIQUE : une seule table pour toutes les commandes
# Les champs communs sont stockés directement, les champs spécifiques
# sont stockés dans ServiceOrderFieldValue
# ==============================================================================

class ServiceOrder(models.Model):

    DELIVERIES = [
        ('Retrait sur place (Dakar)',           'Retrait sur place (Dakar)'),
        ('Livraison à domicile (Dakar)',         'Livraison à domicile (Dakar)'),
        ('Livraison à domicile (Autres régions)','Livraison à domicile (Autres régions)'),
    ]

    # --- Quel service est concerné ---
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='Service'
    )

    # --- Champs communs à tous les services ---
    # Si l'utilisateur upload une image, on la stocke dans le champ "image".
    image = models.ImageField(
        upload_to='Services/orders/',
        verbose_name='Image uploadée',
        null=True, blank=True
        )
    # si l'utilisateur a choisi une des images deja dans la galerie, on stocke le chemin dans img_path (ex: "Services/galerie_image/image1.png")
    img_path = models.CharField(
        max_length=255, blank=True, default='', null=True,
        verbose_name='Chemin de l\'image sélectionnée dans la galerie'
    )
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    quantity      = models.IntegerField(verbose_name='Quantité')
    height        = models.IntegerField(verbose_name='Hauteur (en cm)', null=True, blank=True)
    width         = models.IntegerField(verbose_name='Largeur (en cm)', null=True, blank=True)
    height        = models.IntegerField(verbose_name='Hauteur (en cm)', null=True, blank=True)
    comment       = models.TextField(verbose_name='Instructions spéciales', null=True, blank=True)
    delivery_mode = models.CharField(
        max_length=180,
        choices=DELIVERIES,
        verbose_name='Mode de livraison',
        blank=True
    )

    # --- Informations client ---
    client_name    = models.CharField(max_length=100, verbose_name='Nom du client',    blank=True)
    client_email   = models.EmailField(verbose_name='Email du client',                  blank=True)
    client_phone   = models.CharField(max_length=15,  verbose_name='Téléphone du client', blank=True)
    client_address = models.CharField(max_length=255, verbose_name='Adresse du client', blank=True)

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-created_at']

    def __str__(self):
        return f'Commande #{self.pk} — {self.service} — {self.client_name}'

    def get_img_path(self):
        if self.image:
            try:
                return self.image.url
            except ValueError:
                pass
        return self.img_path or ''


# ==============================================================================
# VALEURS DYNAMIQUES : stocke la valeur de chaque champ spécifique
# pour une commande donnée (pattern Entity-Attribute-Value)
# ==============================================================================

class ServiceOrderFieldValue(models.Model):

    order = models.ForeignKey(
        ServiceOrder,
        on_delete=models.CASCADE,
        related_name='field_values',
        verbose_name='Commande'
    )
    field = models.ForeignKey(
        ServiceField,
        on_delete=models.SET_NULL,
        null=True,
        related_name='values',
        verbose_name='Champ'
    )
    # Toutes les valeurs sont stockées en texte.
    # Pour multicolor : JSON sérialisé  → '["#FF0000", "#0000FF"]'
    # Pour file       : le chemin relatif du fichier uploadé
    # Pour integer    : str(valeur)
    # Pour boolean    : "true" / "false"
    value = models.TextField(verbose_name='Valeur', blank=True, default='')

    class Meta:
        verbose_name = 'Valeur de champ de commande'
        verbose_name_plural = 'Valeurs de champs de commande'

    def __str__(self):
        field_label = self.field.label if self.field else 'Champ supprimé'
        return f'{field_label}'

    def get_typed_value(self):
        """
        Retourne la valeur dans son type Python natif.
        Utile dans les templates et les emails.
        """
        import json
        if not self.field:
            return self.value
        ft = self.field.field_type
        if ft == 'integer':
            try:
                return int(self.value)
            except (ValueError, TypeError):
                return self.value
        if ft == 'boolean':
            return self.value.lower() == 'true'
        if ft == 'multicolor':
            try:
                return json.loads(self.value)   # retourne une liste de hex
            except (ValueError, TypeError):
                return []
        return self.value  # text, select, file → str

    def colored_value(self):
        from django.utils.html import format_html
        import json

        try:
            colors = json.loads(self.value)

            circles = "".join([
                f'''
                <span style="
                    display:inline-block;
                    width:22px;
                    height:22px;
                    border-radius:50%;
                    background:{color};
                    margin-right:6px;
                    border:1px solid #ccc;
                "></span>
                '''
                for color in colors
            ])

            return format_html(circles)

        except:
            return self.value

    colored_value.short_description = 'Valeur du champ'  # Titre de la colonne dans l'admin


# ==============================================================================
# GALERIE D'IMAGES : inchangée
# ==============================================================================

class GalerieImageForService(models.Model):
    service = models.ForeignKey(
        Service,
        max_length=60,
        verbose_name='Service',
        null=True, blank=True,
        related_name='galerie_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='Services/galerie_image',
        default='Services/galerie_image/default3.png',
        verbose_name='Image'
    )

    def __str__(self):
        return f'Image no {self.pk} du service {self.service}'

    class Meta:
        verbose_name = "Image de la galerie pour service"
        verbose_name_plural = "Images de la galerie pour services"