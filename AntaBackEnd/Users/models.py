from django.contrib.auth.models import AbstractUser
from django.db import models
import shortuuid


# Create your models here.

class Fab_User(AbstractUser):

    STATUS = [("Admin","Admin"),
              ("Client","Client")]

    tel_num = models.CharField(max_length=50, null=False, blank=False, verbose_name="Numéro de telephone")
    adress = models.TextField(blank=False, null=False, verbose_name="Adresse")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    status = models.CharField(blank=False, null=False, verbose_name="Statut", max_length=20, choices=STATUS, default="Client")
    uuid = models.CharField(unique=True, blank=True, null=True, max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name


    def save(self, *args, **kwargs):
        # ton code avant la sauvegarde éventuelle
        self.uuid = shortuuid.uuid()
        super().save(*args, **kwargs)  # très important

    class Meta:
        verbose_name = "Utilisateur"

class Order(models.Model):
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
        ('remboursee', 'Remboursée'),
    ]

    number = models.IntegerField(null=False, blank=False, unique=True, verbose_name="Numéro de commande")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de la commande")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours', verbose_name="État de la commande")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True, verbose_name="Facture PDF")

    def __str__(self):
        return f"Commande n°{self.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, verbose_name="Nom du produit")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    def total_price(self):
        return self.quantity * self.price


class Invoice(models.Model):
    pass

# class FavouriteItem(models.Model):
#     pass