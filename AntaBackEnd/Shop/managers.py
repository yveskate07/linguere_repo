from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class OrderManager(models.Manager):
    def create(self, **kwargs):
        from .models import OrderItem
        if 'user' in kwargs:
            # Appeler la méthode create() d’origine
            obj = super().create(**kwargs)

            user = kwargs['user']
            try:
                cart = user.cart
                if cart.total_items == 0:
                    raise ValueError("Le panier est vide.")
                else:
                    for item in cart.items.all():
                        OrderItem.objects.create(
                            order=obj,
                            product=item.product,
                            price=item.product.price,
                            quantity=item.quantity
                        )

            except ObjectDoesNotExist:
                pass # Le panier n'existe pas pour cet utilisateur, donc une commande est créée sans articles.

            return obj
        else:
            raise ValueError("L'utilisateur est requis pour créer une commande.")