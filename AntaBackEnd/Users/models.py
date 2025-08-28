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
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    first_time = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        from Shop.models import Cart

        is_new = self.pk is None  # si l'objet n'a pas encore d'ID

        self.uuid = shortuuid.uuid()

        super().save(*args, **kwargs)  # d'abord on sauvegarde l'utilisateur

        if is_new and self.first_time:
            Cart.objects.create(user=self)
            self.first_time = False
            super().save(update_fields=["first_time"])

    class Meta:
        verbose_name = "Utilisateur"


class Client(models.Model):
    user = models.OneToOneField(Fab_User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    second_name = models.CharField(max_length=100, null=True, blank=True)
    adress = models.CharField(null=True, max_length=200, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_email(self):
        try:
            email = self.user.email
        except:
            email = self.email
        return email

# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('en_cours', 'En cours'),
#         ('expediee', 'Expédiée'),
#         ('livree', 'Livrée'),
#         ('annulee', 'Annulée'),
#         ('remboursee', 'Remboursée'),
#     ]
#
#     number = models.IntegerField(null=False, blank=False, unique=True, verbose_name="Numéro de commande")
#     date = models.DateTimeField(auto_now_add=True, verbose_name="Date de la commande")
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours', verbose_name="État de la commande")
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
#     invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True, verbose_name="Facture PDF")
#
#     def __str__(self):
#         return f"Commande n°{self.number}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.SET_NULL)
#     product_name = models.CharField(max_length=255, verbose_name="Nom du produit")
#     quantity = models.PositiveIntegerField(verbose_name="Quantité")
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
#
#     def __str__(self):
#         return f"{self.quantity} x {self.product_name}"
#
#     def total_price(self):
#         return self.quantity * self.price
#
#
# class Invoice(models.Model):
#     pass

# class FavouriteItem(models.Model):
#     pass