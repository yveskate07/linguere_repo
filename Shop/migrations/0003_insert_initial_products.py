from django.db import migrations, transaction
from django.conf import settings
from pathlib import Path
import json


def insert_products(apps, schema_editor):
    Product = apps.get_model("Shop", "Product")
    path = Path(__file__).resolve().parent.parent.parent / "Json_files" / "shop_product.json"
    with open(path, encoding="utf-8") as f:
        products = json.load(f)

    if not settings.DEBUG:
        for product in products:
            with transaction.atomic():
                Product.objects.update_or_create(
                    reference=product["reference"],
                    defaults=product
                )
        print("Shop Products added successfully")


class Migration(migrations.Migration):

    dependencies = [
        ("Shop", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(insert_products),
    ]
