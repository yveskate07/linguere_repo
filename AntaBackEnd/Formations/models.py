from django.db import models


# Create your models here.
class Formations(models.Model):

    AVAILABILITY = [
        ("online","En ligne"),
        ("in person", "En présentiel"),
        ("both", "Hybride")
    ]

    name = models.CharField(max_length=20)
    duration = models.DurationField() # duree
    motiv = models.TextField() # texte de motivation
    price = models.IntegerField()
    hours_per_week = models.IntegerField()
    availability = models.CharField(choices=AVAILABILITY, max_length=30)

    # doit etre liée à des témoignages

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

class SkillGained(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

class Testimony(models.Model):
    username = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    comment = models.TextField()


