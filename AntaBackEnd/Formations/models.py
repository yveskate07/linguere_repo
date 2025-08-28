import spacy
from django.db import models
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
    motiv = models.TextField() # texte de motivation
    price = models.IntegerField(default=0, null=True, verbose_name='Prix')
    hours_per_week = models.IntegerField(default=0,blank=True, null=True, verbose_name="Nombre d'heures par semaines")
    availability = models.CharField(choices=AVAILABILITY, max_length=30, default='En ligne / Présentiel',blank=True, null=True, verbose_name='Disponibilité')
    slug = models.SlugField(unique=True, blank=True, null=True)
    determinant = models.CharField(max_length=8, default='')
    image = models.ImageField(blank=True,null=True,upload_to='Formations/formation_image', verbose_name='Image descriptive de la formation')

    class Meta:
        verbose_name = 'Formation'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            if not self.determinant:
                if not self.name[0].lower() in ['a','i','u','e','o','y']:
                    nlp = spacy.load("fr_core_news_md")
                    doc = nlp(self.name)
                    for token in doc:
                        genre = token.morph.get("Gender")
                        if genre:
                            if 'Fem' in genre:
                                self.determinant = "la"
                            elif 'Masc' in genre:
                                self.determinant = "le"
                            else:
                                self.determinant=''
                else:
                    self.determinant = "l'"

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

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = "inserer ici le path d'une image par defaut"
        return url

class Module(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name="Nom du module")

    def description(self):
        return f"Module de la Formation {self.formation}"

    description.short_description = "Description"

    class Meta:
        verbose_name = "Modules des formations"
        ordering = ["name"]

class Prerequisites(models.Model): # prerequis pour une formation

    LEVELS = [
        ('Débutant', 'Débutant'),
        ('Amateur', 'Amateur'),
        ('Expert', 'Expert')
    ]

    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    level = models.CharField(choices=LEVELS, max_length=15)
    image = models.ImageField(blank=True, null=True, upload_to='Formations/prerequis_image',
                              verbose_name='Image')


    class Meta:
        verbose_name = "Préréquis par formation"
        ordering = ["name"]

    def __str__(self):
        return self.formation.name + ' - ' + self.name

    def description(self):
        return "Préréquis des Formations"

    description.short_description = "Description"

class SkillGained(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description_skill = models.TextField(blank=True, null=True, default='')

    class Meta:
        verbose_name = "Compétences acquise par formation"
        ordering = ["name"]

    def __str__(self):
        return self.formation.name + ' - ' + self.name

    def description(self):
        return "Compétences gagnées des Formations"

    description.short_description = "Description"

class MotivPoints(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "Motivation"
        ordering = ["name"]

    def __str__(self):
        return 'Pourquoi apprendre '+ self.formation.determinant + ' ' +self.formation.name

class Advantages(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "Avantages de nos formations"
        ordering = ["name"]

    def __str__(self):
        return "Avantages de la formation "+self.formation.name

class Testimony(models.Model):

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30,verbose_name="Statut")
    comment = models.TextField(verbose_name="Commentaire")
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Témoignage"
        #ordering = ["username"]

    def __str__(self):
        return self.username + ' - ' + self.formation

    def description(self):
        return "Témoignages des Formations"

    description.short_description = "Description"

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
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)

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
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, verbose_name='Formation')

    class Meta:
        verbose_name = "Utilisateurs ayant demandé brochure"
        #ordering = ["name"]

    def __str__(self):
        return self.name

    def description(self):
        return f"Utilisateurs ayant telechargé brochures pour la formation {self.formation}"

    description.short_description = "Description"

class UserRequest(models.Model):

    user = models.ForeignKey(Fab_User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE, verbose_name='Formation')

    class Meta:
        verbose_name = "Utilisateurs ayant prit renseignement"
        #ordering = ["name"]

    def __str__(self):
        return self.name

    def description(self):
        return f"Utilisateur ayant prit renseignement pour la formation {self.formation}"

    description.short_description = "Description"