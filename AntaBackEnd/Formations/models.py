from django.db import models
from django.utils.text import slugify


# Create your models here.
class Formations(models.Model):

    AVAILABILITY = [
        ("online","En ligne"),
        ("in person", "En présentiel"),
        ("both", "Hybride")
    ]

    name = models.CharField(max_length=30)
    duration = models.DurationField() # duree
    motiv = models.TextField() # texte de motivation
    price = models.IntegerField(default=0, null=True)
    hours_per_week = models.IntegerField(default=0,blank=True, null=True)
    availability = models.CharField(choices=AVAILABILITY, max_length=30, default='both',blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Formation'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)



class Module(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

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

class SkillGained(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = "Compétences acquise par formation"

    def __str__(self):
        return self.formation + ' - ' + self.name

class Testimony(models.Model):
    username = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    comment = models.TextField()
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Témoignage"

    def __str__(self):
        return self.username + ' - ' + self.formation

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

    name = models.CharField(max_length=50)
    email = models.EmailField()
    tel_number = models.CharField(max_length=20)
    formation_method = models.CharField(choices=FORMATION_METHOD, max_length=30, default='en-ligne')
    session = models.CharField(choices=SESSIONS, max_length=30, default='matin')
    message = models.TextField(blank=True)
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Personnes Inscrite"

    def __str__(self):
        return self.name
    

class UserBrochure(models.Model):

    METHOD = [
        ("en-ligne", "En ligne"),
        ("presentiel", "En présentiel"),
        ("hybride", "Hybride")
    ]

    name = models.CharField(max_length=50)
    email = models.EmailField()
    tel_number = models.CharField(max_length=20)
    method = models.CharField(max_length=20, choices=METHOD, default='en-ligne')
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Utilisateurs ayant demandé brochure"

    def __str__(self):
        return self.name

class UserRequest(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    tel_number = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Utilisateurs ayant prit renseignement"

    def __str__(self):
        return self.name