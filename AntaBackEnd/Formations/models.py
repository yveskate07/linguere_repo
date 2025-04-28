from django.db import models
from django.utils.text import slugify


# Create your models here.
class Formations(models.Model):

    AVAILABILITY = [
        ("online","En ligne"),
        ("in person", "En présentiel"),
        ("both", "Hybride")
    ]

    name = models.CharField(max_length=30, verbose_name='Nom')
    duration = models.DurationField(verbose_name='Durée') # duree
    motiv = models.TextField() # texte de motivation
    price = models.IntegerField(default=0, null=True, verbose_name='Prix')
    hours_per_week = models.IntegerField(default=0,blank=True, null=True, verbose_name="Nombre d'heures par semaines")
    availability = models.CharField(choices=AVAILABILITY, max_length=30, default='both',blank=True, null=True, verbose_name='Disponibilité')
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Formation'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def description(self):
        return "Table des Formations"

    description.short_description = "Description"

class Module(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name="Nom du module")

    def description(self):
        return f"Module de la Formation {self.formation}"

    description.short_description = "Description"

class Prerequisites(models.Model): # prerequis pour une formation

    LEVELS = [
        ('1', 'Débutant'),
        ('2', 'Amateur'),
        ('3', 'Expert')
    ]

    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    level = models.CharField(choices=LEVELS, max_length=15)

    class Meta:
        verbose_name = "Préréquis par formation"

    def __str__(self):
        return self.formation + ' - ' + self.name

    def description(self):
        return "Préréquis des Formations"

    description.short_description = "Description"

class SkillGained(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "Compétences acquise par formation"

    def __str__(self):
        return self.formation + ' - ' + self.name

    def description(self):
        return "Compétences gagnées des Formations"

    description.short_description = "Description"

class Testimony(models.Model):

    username = models.CharField(max_length=30,verbose_name="Nom d'utiisateur")
    status = models.CharField(max_length=30,verbose_name="Statut")
    comment = models.TextField(verbose_name="Commentaire")
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Témoignage"

    def __str__(self):
        return self.username + ' - ' + self.formation

    def description(self):
        return "Témoignages des Formations"

    description.short_description = "Description"

class SignedUpUser(models.Model):

    FORMATION_METHOD = [
        ("en-ligne", "En ligne"),
        ("presentiel", "En présentiel"),
        ("hybride", "Hybride")
    ]

    SESSIONS = [
        ('matin', 'Matin (9h-12h)'),
        ('apres-midi', 'Après-midi (14h-17h)'),
        ('soir', 'Soir (18h-21h)')
    ]

    name = models.CharField(max_length=50, verbose_name="Nom")
    email = models.EmailField()
    tel_number = models.CharField(max_length=20, verbose_name="Téléphone")
    formation_method = models.CharField(choices=FORMATION_METHOD, max_length=30, default='en-ligne', verbose_name="Méthode de formation")
    session = models.CharField(choices=SESSIONS, max_length=30, default='matin')
    message = models.TextField(blank=True)
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Personnes Inscrite"

    def __str__(self):
        return self.name

    def description(self):
        return f"Utilisateur inscrit à la formation {self.formation}"

    description.short_description = "Description"
    

class UserBrochure(models.Model):

    METHOD = [
        ("en-ligne", "En ligne"),
        ("presentiel", "En présentiel"),
        ("hybride", "Hybride")
    ]

    name = models.CharField(max_length=50, verbose_name='Nom')
    email = models.EmailField()
    tel_number = models.CharField(max_length=20, verbose_name='Téléphone')
    message = models.TextField(blank=True, null=True)
    method = models.CharField(max_length=20, choices=METHOD, default='en-ligne', verbose_name='Méthode de formation')
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, verbose_name='Formation')

    class Meta:
        verbose_name = "Utilisateurs ayant demandé brochure"

    def __str__(self):
        return self.name

    def description(self):
        return f"Utilisateurs ayant telechargé brochures pour la formation {self.formation}"

    description.short_description = "Description"

class UserRequest(models.Model):

    name = models.CharField(max_length=50, verbose_name='Nom')
    email = models.EmailField()
    tel_number = models.CharField(max_length=20, verbose_name='Téléphone')
    message = models.TextField(blank=True)
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, verbose_name='Formation')

    class Meta:
        verbose_name = "Utilisateurs ayant prit renseignement"

    def __str__(self):
        return self.name

    def description(self):
        return f"Utilisateur ayant prit renseignement pour la formation {self.formation}"

    description.short_description = "Description"