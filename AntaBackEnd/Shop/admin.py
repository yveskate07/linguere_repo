from django.contrib import admin
from Shop.models import Product, Order, Invoice
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'badge', 'stock', 'main_category', 'category', 'disponibility')
    fields = ('image','name', 'description', 'price', 'badge', 'stock', 'main_category', 'category', 'disponibility')

    list_per_page = 60

    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "status", "user", 'complete')
    fields = ("date", "status", "user", 'delivery_price', 'complete')

    search_fields = ("id", "user__username", "user__email")
    list_filter = ("status",  "date", 'complete')

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