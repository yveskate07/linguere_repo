from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from Shop.models import Product, Order, Invoice, Payment
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'badge', 'stock', 'main_category', 'category', 'disponibility')
    fields = ('image','name', 'description', 'price', 'badge', 'stock', 'main_category', 'category', 'disponibility')

    list_per_page = 60

    search_fields = ('name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    change_list_template = "admin/Shop/order/change_list.html"
    list_display = ('payment_date', 'order', 'total_amount', 'payment_method', )
    fields = ('total_amount', 'payment_method', )

    list_filter = ('payment_method', )

    search_fields = ('order__id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("get_id","date", "status", "total_price", "user")
    fields = ('delivery_price', "status", 'complete')

    search_fields = ("id", "user__username", "user__email")
    list_filter = ("status",  "date", 'complete')

    def save_model(self, request, obj, form, change):
        if obj.status == 'Payée':

            obj.complete = True
            obj.save()
            # create a payment record here
            payment = Payment.objects.create(order=obj, total_amount=obj.total_price, payment_method='Admin', done=True)
            self._redirect_payment_id = payment.id


        super().save_model(request, obj, form, change)

    def response_change(self, request, obj):

        # redirection si on a modifié le status à 'Payée'
        if hasattr(obj, 'payment') and obj.status == 'Payée':

            payment_id = self._redirect_payment_id
            del self._redirect_payment_id
            url = reverse('admin:Shop_payment_change', args=[payment_id])

            return redirect(url)
        # sinon réponse normale

        return super().response_change(request, obj)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}

        # Build an HTML table describing all orders and their items
        html = """
        <div style="background:#f7f9fb; padding:15px; border-radius:8px; border:1px solid #ddd; margin-bottom:20px;">
            <h2 style="margin-top:0; color:#2c3e50;">📦 Aperçu de la commande</h2>
            <p>Ci-dessous est un aperçu de toutes les articles de cette commande.</p>
        """

        try:
            order = Order.objects.get(pk=object_id)

        except Order.DoesNotExist:

            order = None

        if not order:
            html += "<p><em>Cette commande n'existe pas.</em></p>"
        else:
            html += f"""
                <div style="margin-top:10px; padding:10px; background:#fff; border:1px solid #eee; border-radius:5px;">
                    <h3 style="color:#007bff;">Commande #{order.id} — ({order.status})</h3>
                    <table style="width:100%; border-collapse:collapse; margin-top:10px;">
                        <thead>
                            <tr style="background:#f0f4f8;">
                                <th style="text-align:left; padding:5px; border-bottom:1px solid #ccc;">Produit</th>
                                <th style="text-align:right; padding:5px; border-bottom:1px solid #ccc;">Quantité</th>
                                <th style="text-align:right; padding:5px; border-bottom:1px solid #ccc;">Prix unitaire</th>
                                <th style="text-align:right; padding:5px; border-bottom:1px solid #ccc;">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                """

            total_price = 0
            for item in order.order_item.all():
                product_name = item.product.name if item.product else "Produit supprimé"
                item_total = float(item.total)
                total_price += item_total

                html += f"""
                        <tr>
                            <td style="padding:5px;">{product_name}</td>
                            <td style="padding:5px; text-align:right;">{item.quantity}</td>
                            <td style="padding:5px; text-align:right;">{item.price} FCFA</td>
                            <td style="padding:5px; text-align:right;">{item_total:.2f} FCFA</td>
                        </tr>
                    """

            html += f"""
                        </tbody>
                    </table>
                    <p style="text-align:right; font-weight:bold; color:#27ae60; margin-top:10px;">
                        Total: {total_price:.2f} FCFA
                    </p>
                </div>
                """

        html += "</div>"

        # Make HTML safe for Django to render

        extra_context["description"] = mark_safe(html)
        return super().change_view(request, extra_context=extra_context, object_id=object_id, form_url=form_url)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'invoice_date_time',
        'total',
        'last_updated_date',
        'paid',
        'invoice_type')

admin.site.site_title = _('LINGUERE FABLAB')
admin.site.site_header = _('LINGUERE FABLAB')
admin.site.index_title = _('LINGUERE FABLAB ADMINISTRATION')