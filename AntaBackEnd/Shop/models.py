import django.utils.timezone
import shortuuid
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from AntaBackEnd import settings
from Users.models import Fab_User, Client
import pdfkit
import os
from django.template.loader import render_to_string, get_template

path_wkhtmltopdf = r"C:\Program Files\wkhtlmtopdf\wkhtmltox\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


class Product(models.Model):
    BADGES = [("Nouveau","Nouveau"),
              ("Top ventes","Top ventes"),
              ("Promo","Promo")]
    CATEGORIES = [("Kits Arduino","Kits Arduino"),
                  ("Composants IOT","Composants IOT"),
                  ("Robotique","Robotique"),
                  ("Capteurs","Capteurs")]

    DISPONIBILITY = [("En stock","En stock"),
                     ("Stock limité","Stock limité"),
                     ("Rupture de stock","Rupture de stock")]

    MAIN_CATEGORIES = [("Kits Arduino et IOT","Kits Arduino et IOT"),
                       ("Machines Numériques","Machines Numériques"),
                       ("Installations Fablab","Installations Fablab")]

    reference = models.CharField(verbose_name='Reference', max_length=100, blank=False, null=False)
    image = models.ImageField(verbose_name="Image", blank=False, null=False, upload_to="Shop/Products_images")
    name = models.CharField(blank=False, null=False, verbose_name="Nom du produit", max_length=60, unique=True)
    description = models.CharField(blank=False, null=False, verbose_name="Description", max_length=240)
    badge = models.CharField(verbose_name="Badge", blank=True, null=True, max_length=60, choices=BADGES)
    price = models.IntegerField(verbose_name="Prix", blank=False, null=False)
    stock = models.IntegerField(verbose_name="En stock", blank=False, null=False)
    main_category = models.CharField(verbose_name="Categorie principale", blank=False, null=False, max_length=60, choices=MAIN_CATEGORIES)
    category = models.CharField(verbose_name="Catégorie", blank=False, null=False, max_length=60, choices=CATEGORIES)
    disponibility = models.CharField(verbose_name="Disponibilité", blank=False, null=False, max_length=60, choices=DISPONIBILITY)
    added_date = models.DateTimeField(verbose_name="Date d'ajout", default=timezone.now)
    image_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="URL de l'image", default='')

    class Meta:
        verbose_name = "Produit"
        ordering = ["-added_date"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if self.image:
            self.image_url = self.image.url
        else: 
            self.image_url = 'mettre ici un lien par defaut'
            
        super().save(*args, **kwargs)  # On sauvegarde d'abord le produit (important pour avoir self.pk)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = "inserer ici le path d'une image par defaut"
        return url


class Cart(models.Model):

    user = models.OneToOneField(Fab_User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cart')
    session_token = models.CharField(max_length=256, null=True, default='', verbose_name='Token Session')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def to_dict(self):
        return {
            "products": [item.to_dict for item in self.items.all()],
            "total_price": self.total_price,
        }

    def __str__(self):
        return f"Panier de {self.user.username} / id : {self.id}"

    def save(self,*args,**kwargs):
        self.updated_at = django.utils.timezone.now()
        
        super().save(*args, **kwargs)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', null=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} et id:{self.id}"

    @property
    def to_dict(self):
        return {
            "id": self.product.id,
            "name": self.product.name,
            "price": self.product.price,
            "category": self.product.category,
            "image": self.product.imageURL if self.product.image else None,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "item_id": self.id
        }

class Order(models.Model):
    STATUS_CHOICES = [
        ('En cours', 'En cours'),
        ('Expédiée', 'Expédiée'),
        ('Livrée', 'Livrée'),
        ('Annulée', 'Annulée'),
        ('Remboursée', 'Remboursée'),
    ]

    PAYMENT_METHOD = [
        ('Orange Money', 'Orange Money'),
        ('Wave', 'Wave')
    ]

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de la commande")
    total_amount = models.IntegerField(verbose_name="Montant total")
    complete = models.BooleanField(default=False, null=True, blank=True, verbose_name='Finalisée')
    transaction_id = models.CharField(max_length=200, unique=True)
    echeance_payment = models.IntegerField(null=False, blank=False, verbose_name="Échéance de paiement en jour", default=7) 
    payment_token = models.CharField(max_length=500, unique=True, verbose_name='Token de payment CINETPAY', default='')
    payment_url = models.CharField(max_length=500, unique=True, verbose_name='Url de payment CINETPAY', default='')
    api_response_id = models.CharField(max_length=500, unique=True, verbose_name='id reponse CINETPAY', default='')
    tracking_number = models.CharField(max_length=200, null=True, blank=True, verbose_name="Numéro de suivi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En cours',
                              verbose_name="État de la commande")
    payment_method = models.CharField(max_length=50, null=True, blank=True, verbose_name="Méthode de paiement",
                                      choices=PAYMENT_METHOD, default='Wave')
    delivery_price = models.IntegerField(default=0, verbose_name="Frais de livraison")

    def __str__(self):
        return f"Commande N° {self.id}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Pour obtenir un id

        if is_new and not self.transaction_id:
            print("Creating transaction ID because it's a new order")
            self.transaction_id = f"{shortuuid.uuid()}-{self.id}"
            super().save(update_fields=["transaction_id"])

        if self.complete:
            print("Order is marked as complete. Processing order items and updating status.")
            self.status = 'Expédiée'

            print('changing order status to Expédiée')

            cart_items = self.user.cart.items.all()
            print(f"getting cart items for user: {cart_items}")

            print('user is :', self.user)

            # Crée des OrderItem à partir des CartItems du panier du user
            for item in cart_items:
                OrderItem.objects.create(
                    order=self,
                    product=item.product,
                    price=item.product.price,  # ou item.price si tu veux figer une promo
                    quantity=item.quantity
                )

            # generation de la facture
            invoice = Invoice(
                user=self.user,
                subtotal=self.total_amount - self.delivery_price,
                tax_amount=12,  # Exemple de TVA
                discount=0,  # Exemple de remise
                total=self.total_amount,
                order=self
            )
            invoice.save()  # Sauvegarde pour générer le PDF
            # Vider le panier de l'utilisateur
            cart_items.delete()

            super().save(update_fields=["status"])
        else:
            print("Order is not complete. No further processing needed.")

    def send_confirmation(self, text_content, template_name, context, subject, to_email):
        context['products'] = self.order_item.all()
        html_content = render_to_string(template_name, context)

        # envoi du mail avec le template HTML
        email = EmailMultiAlternatives(subject=subject,
                                       body=text_content,
                                       from_email=settings.EMAIL_HOST_USER,
                                       to=[to_email])

        email.attach_alternative(html_content, "text/html")

        try:
            result = email.send(fail_silently=False)
            if result:
                return True
            else:
                return False
        except Exception as e:
            return f"❌ Erreur lors de l’envoi du mail : {e}"

    @property
    def admin_link(self):
        # Génère l’URL pour modifier cet objet dans l’admin
        url = reverse(
            f'admin:{self._meta.app_label}_{self._meta.model_name}_change',
            args=[self.pk]
        )

        absolute_url = f"{settings.DOMAIN_NAME}{url}"

        return absolute_url


class Invoice(models.Model):

    """
    Name: Invoice model definition
    Description:
    Author: kateyveschadrac@gmail.com
    """

    INVOICE_TYPES = [
        ('RECEIPT','RECEIPT'),
        ('PROFORMA INVOICE','PROFORMA INVOICE'),
        ('INVOICE','INVOICE')
    ]

    user = models.ForeignKey(Fab_User, on_delete=models.SET_NULL, null=True, verbose_name='Client')
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    rccm_number = models.CharField(max_length=160, verbose_name='Numéro Registre de Commerce et du Crédit Mobilier', null=True, blank=True, default='Numéro Registre de Commerce et du Crédit Mobilier')
    ninea_number = models.CharField(max_length=160, verbose_name='Numéro d’Identification Nationale des Entreprises et Associations', null=True, blank=True, default='Numéro d’Identification Nationale des Entreprises et Associations')
    #reference = models.CharField(max_length=100,null=True,blank=True,verbose_name="Référence commande / projet")
    due_date = models.DateField(null=True,blank=True,verbose_name="Date d’échéance")
    last_updated_date = models.DateTimeField(null=True,blank=True,verbose_name='Dernière modification')
    subtotal = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="Sous-total HT")  # Montant avant taxes
    tax_amount = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="TVA en pourcentage (%)")  # TVA calculée
    discount = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="Remise")
    total = models.DecimalField(max_digits=12,decimal_places=2,verbose_name='Total TTC',default=0)
    paid = models.BooleanField(default=False, verbose_name='Payé')
    invoice_type = models.CharField(max_length=60, choices=INVOICE_TYPES, verbose_name='Type de facture', default='PROFORMA INVOICE')
    comment = models.TextField(null=True, max_length=1000, blank=True, verbose_name='Merci pour votre confiance.')
    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True, verbose_name="Facture PDF")
    order = models.ForeignKey(Order, verbose_name='Order', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-invoice_date_time']

    def __str__(self):
        return f'Invoice No {self.id} / {self.user.name}_{self.invoice_date_time}'

    @property
    def tax_value(self):
        return (self.subtotal * Decimal(self.tax_amount)) / Decimal(100)

    @property
    def discount_value(self):
        return (self.subtotal * Decimal(self.discount)) / Decimal(100)

    @property
    def total_with_taxes(self):
        return self.subtotal + self.tax_value - self.discount_value

    def save(self, *args, **kwargs):
        # Convertir pour éviter les erreurs de type
        subtotal = Decimal(self.subtotal)
        tax = Decimal(self.tax_amount) / Decimal(100)
        discount = Decimal(self.discount) / Decimal(100)

        # Calcul du total TTC avec remise
        self.total = subtotal * (1 + tax) * (1 - discount)

        # Met à jour la date de modification
        self.last_updated_date = timezone.now()

        super().save(*args, **kwargs)

        # Sauvegarder la référence du fichier dans le champ FileField
        self.invoice_pdf.name = f"invoices/invoice_{self.id}.pdf"

        super().save(update_fields=['invoice_pdf'])

        html_template = get_template("Shop/invoice/invoice.html")
        # Générer le HTML avec Django
        html = html_template.render(context={"invoice": self, 'orderitem_set':self.order.order_item.all() ,'logo_path': f"{settings.DOMAIN_NAME}/{settings.STATIC_URL}AntaBackend/images/logos.jpeg"})

        # Chemin du fichier PDF
        pdf_path = os.path.join(settings.MEDIA_ROOT, "invoices", f"invoice_{self.id}.pdf")

        option = {'page-size': 'Letter',
                  'encoding': "UTF-8",
                  'margin-top': '0.75in',
                  'margin-right': '0.75in',
                  'margin-bottom': '0.75in',
                  'margin-left': '0.75in',
                  }

        # Générer PDF avec pdfkit
        pdfkit.from_string(html, pdf_path, options=option, configuration=config)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_item')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    quantity = models.IntegerField(verbose_name='Quantité')

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    @property
    def total(self):
        return self.quantity * self.price

class AddressChipping(models.Model):

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    commande = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    adress = models.CharField(max_length=100, null=True)
    ville = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adress