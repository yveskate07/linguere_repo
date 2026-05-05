from django.db import models

# Create your models here.
class ImagesOnHomepage(models.Model):
    image1 = models.ImageField(upload_to='homepage_images/', verbose_name='Image 1', blank=True, null=True)
    image2 = models.ImageField(upload_to='homepage_images/', verbose_name='Image 2', blank=True, null=True)
    image3 = models.ImageField(upload_to='homepage_images/', verbose_name='Image 3', blank=True, null=True)
    

    def __str__(self):
        return f"Personalizations {self.id}"
    
    @property
    def name(self):
        return f"Images sur la page d'accueil"
    
    class Meta:
        verbose_name = "Personalization"
        verbose_name_plural = "Personalizations"