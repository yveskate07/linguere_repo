from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from Users.models import Fab_User

# Create your models here.
class Formations(models.Model):

    AVAILABILITY = [
        ("En ligne","En ligne"),
        ("En présentiel","En présentiel"),
        ("En ligne / Présentiel", "En ligne / Présentiel")
    ]

    name = models.CharField(max_length=30, verbose_name='Nom')
    duration = models.DurationField(verbose_name='Durée') # duree
    description_accueil = models.TextField(blank=False, null=False, verbose_name="Description sur page accueil")
    price = models.IntegerField(default=0, null=True, verbose_name='Prix')
    hours_per_week = models.IntegerField(default=0,blank=True, null=True, verbose_name="Nombre d'heures par semaines")
    availability = models.CharField(choices=AVAILABILITY, max_length=30, default='En ligne / Présentiel',blank=True, null=True, verbose_name='Disponibilité')
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(blank=True,null=True,upload_to='Formations/formation_image', verbose_name='Image descriptive de la formation')
    url_name = models.CharField(blank=False, null=False, verbose_name="Nom de l'url", max_length=120)
    image_home = models.ImageField(blank=True,null=True,upload_to='Formations/formation_image', verbose_name='Image de la formation sur page accueil')
    why_image = models.ImageField(blank=True,null=True,upload_to='Formations/formation_image', verbose_name='Image Pourquoi cette formation ?')

    class Meta:
        verbose_name = 'Formation'
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def get_absolut_url(self):
        return reverse(f'{self.url_name}')

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_duration_display_fr(self):
        total_seconds = self.duration.total_seconds()
        days = self.duration.days
        hours = int((total_seconds % 86400) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{days} jour{'s' if days > 1 else ''}, {hours:02}:{minutes:02}:{seconds:02}"

    def description(self):
        return "Table des Formations"

    description.short_description = "Description"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = "inserer ici le path d'une image par defaut"
        return url

    @property
    def imageHomeUrl(self):
        try:
            url = self.image_home.url
        except:
            url = "inserer ici le path d'une image par defaut",
        return url

    @property
    def why_img_url(self):
        try:
            url = self.why_image.url
        except:
            url = "inserer ici le path d'une image par defaut",
        return url

class Module(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, related_name='Modules')
    name = models.CharField(max_length=120, verbose_name="Nom du module")

    def description(self):
        return f"Module de la Formation {self.formation}"

    description.short_description = "Description"

    class Meta:
        verbose_name = "Module de formation"
        verbose_name_plural = "Modules principaux"
        ordering = ["name"]

class Prerequisites(models.Model): # prerequis pour une formation

    LEVELS = [
        ('Débutant', 'Débutant'),
        ('Amateur', 'Amateur'),
        ('Expert', 'Expert')
    ]

    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, related_name='Prerequisites')
    name = models.CharField(max_length=30)
    level = models.CharField(choices=LEVELS, max_length=15)
    image = models.ImageField(blank=True, null=True, upload_to='Formations/prerequis_image',
                              verbose_name='Image')


    class Meta:
        verbose_name = "Préréquis par formation"
        verbose_name_plural = "Maîtrise les Technologies & Compétences Essentielles"
        ordering = ["name"]

    def __str__(self):
        return self.formation.name + ' - ' + self.name

    def description(self):
        return "Préréquis des Formations"

    description.short_description = "Description"

class SkillGained(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, related_name='SkillsGained')
    name = models.CharField(max_length=30)
    description_skill = models.TextField(blank=True, null=True, default='')

    class Meta:
        verbose_name = "Compétences acquise par formation"
        verbose_name_plural = "Ce Que Vous Allez Acquérir"
        ordering = ["name"]

    def __str__(self):
        return self.formation.name + ' - ' + self.name

    def description(self):
        return "Compétences gagnées des Formations"

    description.short_description = "Description"

class MotivPoints(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, related_name='MotivPoints')
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "Motivation"
        verbose_name_plural = "Pourquoi suivre cette formation ?"
        ordering = ["name"]

    def __str__(self):
        return 'Pourquoi se former en ' +self.formation.name

class Advantages(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, related_name='Advantages')
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "Avantage de notre formation"
        verbose_name_plural = "Pourquoi Choisir Notre Formation ?"
        ordering = ["name"]

    def __str__(self):
        return "Avantages de la formation "+self.formation.name

"""class Testimony(models.Model):

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30,verbose_name="Statut")
    comment = models.TextField(verbose_name="Commentaire")
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, related_name='Testimonies')

    class Meta:
        verbose_name = "Témoignage"
        #ordering = ["username"]

    def __str__(self):
        return self.username + ' - ' + self.formation

    def description(self):
        return "Témoignages des Formations"

    description.short_description = "Description"""

class SignedUpUser(models.Model):

    AVAILABILITY = [
        ("En ligne", "En ligne"),
        ("En présentiel", "En présentiel"),
        ("En ligne / Présentiel", "En ligne / Présentiel")
    ]

    SESSIONS = [
        ('Matin (9h-12h)', 'Matin (9h-12h)'),
        ('Après-midi (14h-17h)', 'Après-midi (14h-17h)'),
        ('Soir (18h-21h)', 'Soir (18h-21h)')
    ]

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)
    availability = models.CharField(choices=AVAILABILITY, max_length=30, default='En ligne / Présentiel', verbose_name="Disponibilité")
    session = models.CharField(choices=SESSIONS, max_length=30, default='Matin (9h-12h)')
    message = models.TextField(blank=True)
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, related_name='SignedUpUsers')

    class Meta:
        verbose_name = "Personnes Inscrite"
        #ordering = ["name"]

    def __str__(self):
        return self.name

    def description(self):
        return f"Utilisateur inscrit à la formation {self.formation}"

    description.short_description = "Description"

class UserBrochure(models.Model):

    AVAILABILITY = [
        ("En ligne", "En ligne"),
        ("En présentiel", "En présentiel"),
        ("En ligne / Présentiel", "En ligne / Présentiel")
    ]

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    availability = models.CharField(max_length=22, choices=AVAILABILITY, default='En ligne', verbose_name='Méthode de formation')
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, verbose_name='Formation', related_name='UserBrochures')

    class Meta:
        verbose_name = "Demandes de brochures"
        #ordering = ["name"]

    def __str__(self):
        return self.user.name

    def description(self):
        return f"Utilisateurs ayant telechargé brochures pour la formation {self.formation}"

    description.short_description = "Description"

class UserRequest(models.Model):

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, verbose_name='Formation', related_name='UserRequest')

    class Meta:
        verbose_name = "Demandes de renseignements"
        #ordering = ["name"]

    def __str__(self):
        return self.name

    def description(self):
        return f"Utilisateur ayant prit renseignement pour la formation {self.formation}"

    description.short_description = "Description"