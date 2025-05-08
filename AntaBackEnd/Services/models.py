from django.db import models

# Create your models here.
class Service(models.Model):

    name = models.CharField(max_length=30, verbose_name='Nom')
    description = models.TextField(verbose_name='Description')
    image1 = models.ImageField(blank=True,null=True,upload_to='Services/service_image', verbose_name='Image 1')
    image2 = models.ImageField(blank=True,null=True,upload_to='Services/service_image', verbose_name='Image 2')
    image3 = models.ImageField(blank=True,null=True,upload_to='Services/service_image', verbose_name='Image 3')
    image4 = models.ImageField(blank=True,null=True,upload_to='Services/service_image', verbose_name='Image 4')


class Commande(models.Model):
    pass

class CustomizedServices(models.Model):
    pass
