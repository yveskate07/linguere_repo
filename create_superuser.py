import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AntaBackEnd.settings")
django.setup()

# displaying if wether we are using a sqlite3 database or postgresql database
#print(f"database used is {settings.DATABASES}")

User = get_user_model()


try:
    User.objects.get(username="yveskate07", is_superuser=True)
    """print("Truncating the table Users_fab_user...")
    # because we have sometimes this error : django.db.utils.IntegrityError: duplicate key value violates unique constraint "Users_fab_user_pkey"
    # we need to truncate the table of the users
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE "Users_fab_user" RESTART IDENTITY CASCADE;')
    print("Superuser n'existe pas.")"""
except User.DoesNotExist:
    User.objects.create_superuser(first_name="yves", last_name="kate",username="yveskate07" ,tel_num="+221781586866" ,adress="Senegal" , email="kateyveschadrac@gmail.com", password="azerty12345")
    print("Superuser créé !")
else:
    print("Superuser existe déjà.")

try:
    User.objects.get(username="linguerefablab221")
    """print("Truncating the table Users_fab_user...")
    # because we have sometimes this error : django.db.utils.IntegrityError: duplicate key value violates unique constraint "Users_fab_user_pkey"
    # we need to truncate the table of the users
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE "Users_fab_user" RESTART IDENTITY CASCADE;')
    print("Superuser n'existe pas.")"""
except User.DoesNotExist:
    User.objects.create_superuser(first_name="Anta", last_name="Ngom",username="linguerefablab221" ,tel_num="+221773146662" ,adress="Senegal" , email="linguerefablab@gmail.com", password="azerty12345")
    print("Linguere user créé !")
else:
    print("Linguere user existe déjà.")