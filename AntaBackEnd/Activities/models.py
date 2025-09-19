from django.db import DJANGO_VERSION_PICKLE_KEY, models

# Create your models here.
class Activity(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Activité")
    description = models.TextField(null=True, blank=True, verbose_name="Description de l'activité")
    description_accueil = models.TextField(null=True, blank=True, verbose_name="Description courte pour l'accueil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    presentation_img = models.ImageField(upload_to='activity_images/', null=True, blank=True, verbose_name="Image accueil")
    motiv1 = models.TextField(null=True, blank=True, verbose_name="Motivation 1")
    motiv2 = models.TextField(null=True, blank=True, verbose_name="Motivation 2")
    url_name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name="Nom de l'URL")


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse(f'{self.url_name}')
    
    @property
    def get_image_url(self):
        if self.presentation_img:
            return self.presentation_img.url
        return None
    
    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['-created_at']

class Realisation(models.Model):
    categories = [
        ('Ateliers Réguliers', 'Ateliers Réguliers'),
        ('Compétitions', 'Compétitions'),
        ('FabLabs Équipés', 'FabLabs Équipés'),
    ]

    description = models.TextField(null=True, blank=True, verbose_name="Description de la réalisation")
    category = models.CharField(max_length=50, choices=categories, null=False, blank=False, verbose_name="Catégorie de la réalisation")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='realisations', verbose_name="Activité")
    stat1 = models.IntegerField(null=True, blank=True, verbose_name="Statistique 1")
    stat2 = models.IntegerField(null=True, blank=True, verbose_name="Statistique 2")

    def __str__(self):
        return self.activity.name + ' / ' +self.category

class Resultat(models.Model):
    description = models.TextField(null=True, blank=True, verbose_name="Description du résultat")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='resultats', verbose_name="Activité")
    image = models.ImageField(upload_to='resultat_images/', null=True, blank=True, verbose_name="Image du résultat")
    stat1 = models.IntegerField(null=True, blank=True, verbose_name="Statistique 1")
    stat2 = models.IntegerField(null=True, blank=True, verbose_name="Statistique 2")
    stat3 = models.IntegerField(null=True, blank=True, verbose_name="Statistique 3")
    stat4 = models.IntegerField(null=True, blank=True, verbose_name="Statistique 4")

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    def __str__(self):
        return self.activity.name + ' : Resultats'


class Impact(models.Model):
    categories = [
        ('Éducation Numérique', 'Éducation Numérique'),
        ('Projets Innovants', 'Projets Innovants'),
        ('Impact Communautaire', 'Impact Communautaire'),
    ]
    categorie = models.CharField(max_length=50, choices=categories, null=False, blank=False, verbose_name="Catégorie de l'impact")
    description = models.TextField(null=True, blank=True, verbose_name="Description de l'impact")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='impacts', verbose_name="Activité")

    def __str__(self):
        return self.activity.name + ' / ' +self.categorie


class ActivityGalerieImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='galerie_images', verbose_name="Activité")
    image = models.ImageField(upload_to='activity_galerie/', null=False, blank=False, verbose_name="Image de la galerie")
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom de l'image")
    description = models.TextField(null=True, blank=True, verbose_name="Description de l'image")

    def __str__(self):
        return self.activity.name + ' / ' +self.name
    
    class Meta:
        verbose_name = "Images de la galerie"