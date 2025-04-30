import spacy
from django.db import models
from django.utils.text import slugify


# Create your models here.
class Formations(models.Model):

    AVAILABILITY = [
        ("En ligne","online"),
        ("En présentiel","in person"),
        ("En ligne / Présentiel", "both")
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
    image = models.ImageField(blank=True, null=True, upload_to='Formations/prerequis_image',
                              verbose_name='Image')


    class Meta:
        verbose_name = "Préréquis par formation"

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
        verbose_name = "Motivations"

    def __str__(self):
        return 'Pourquoi apprendre '+ self.formation.determinant + ' ' +self.formation.name

class Advantages(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "Avantages de nos formations"

    def __str__(self):
        return "Avantages de la formation "+self.formation.name

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