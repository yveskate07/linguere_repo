from django.contrib import admin
from django.utils.safestring import mark_safe

from Services.models import *


class GalerieImageForServiceInline(admin.TabularInline):
    model = GalerieImageForService

@admin.register(CustomizedService)
class CustomizedServiceAdmin(admin.ModelAdmin):
    list_display = ('get_id','user','service','adress_delivery','delivery_mode')

    search_fields = ("id",)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        # Build an HTML table describing the orders 
        html = """
        <div style="background:#f7f9fb; padding:15px; border-radius:8px; border:1px solid #ddd; margin-bottom:20px;">
            <h2 style="margin-top:0; color:#2c3e50;">📦 Aperçu de la commande</h2>
            <p>Ci-dessous est un aperçu de la commande.</p>
        """

        try:
            order = CustomizedService.objects.get(pk=object_id)
        except CustomizedService.DoesNotExist:
            order = None

        if not order:
            html += "<p><em>Cette commande n'existe pas.</em></p>"
        else:
            html += f"""
                <div style="margin-top:10px; padding:10px; background:#fff; border:1px solid #eee; border-radius:5px;">
                    <h3 style="color:#007bff;">Commande #{order.id}</h3>
                    <table style="width:100%; border-collapse:collapse; margin-top:10px;">
                        <thead>
                            <tr style="background:#f0f4f8;">
                                <th style="text-align:left; padding:5px; border-bottom:1px solid #ccc;">CLient</th>
                                <th style="text-align:right; padding:5px; border-bottom:1px solid #ccc;">Personnalisation</th>
                                <th style="text-align:right; padding:5px; border-bottom:1px solid #ccc;">Image</th>
                                <th style="text-align:right; padding:5px; border-bottom:1px solid #ccc;">Lieu de livraison</th>
                            </tr>
                        </thead>
                        <tbody>
                """
            
            client = order.user.first_name + "<br>" + order.user.last_name + "<br>" + order.user.email + "<br>" + order.user.tel_num if order.user else "Utilisateur supprimé"

            personnalisation = "<br>".join([f"{key} : {value}" for key, value in order.fields_value.items()]) if order.fields_value else "Aucune personnalisation"

            image = f'<img src="{order.chosen_picture}" alt="Image choisie" style="max-width:100px; max-height:100px;">' if order.chosen_picture else f'<img src="{order.imported_picture.url}" alt="Image importée" style="max-width:100px; max-height:100px;">' if order.imported_picture else "Aucune image"

            lieu_livraison = order.adress_delivery if order.adress_delivery else "Non spécifié"

            html += f"""
                        <tr>
                            <td style="padding:5px;">{client}</td>
                            <td style="padding:5px; text-align:right;">{personnalisation}</td>
                            <td style="padding:5px; text-align:right;">{image} FCFA</td>
                            <td style="padding:5px; text-align:right;">{lieu_livraison} FCFA</td>
                        </tr>
                    """
            
            html += f"""
                        </tbody>
                    </table>
                </div>
                """

        html += "</div>"

        extra_context["description"] = mark_safe(html)
        return super().change_view(request, extra_context=extra_context, object_id=object_id, form_url=form_url)

class FieldForServiceInline(admin.TabularInline):
    model = FieldForService

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('name','description', 'description_accueil','slug',)
    readonly_fields = ('slug',)
    inlines = [GalerieImageForServiceInline, FieldForServiceInline]
    list_display = ('name','description',)
