from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Testimony(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, verbose_name='Nom')
    testimony = models.TextField(null=False, blank=False, verbose_name='Témoignage')
    picture = models.ImageField(upload_to='testimonies_pictures/', null=False, blank=False, verbose_name='Image')
    user_short_description = models.CharField(max_length=30, null=False, blank=False, verbose_name='Courte Description')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # seulement à la création
            if Testimony.objects.count() >= 3:
                raise ValidationError("Maximum de 3 instances atteint.")
        super().save(*args, **kwargs)

    def clean(self):
        if not self.pk and Testimony.objects.count() >= 3:
            raise ValidationError("Maximum de 3 instances atteint.")