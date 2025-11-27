import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AntaBackEnd.settings")
django.setup()


# displaying if wether we are using a sqlite3 database or postgresql database
print(f"database used is {settings.DATABASES}")

User = get_user_model()

# displaying all the users in the database
print("Users in the database :")
for user in User.objects.all():
    print(user)

if not User.objects.filter(username="linguerefablab", is_superuser=True).exists():
    print("Truncating the table Users_fab_user...")
    # because we have sometimes this error : django.db.utils.IntegrityError: duplicate key value violates unique constraint "Users_fab_user_pkey"
    # we need to truncate the table of the users
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE Users_fab_user RESTART IDENTITY CASCADE;")
    print("Superuser n'existe pas.")
    User.objects.create_superuser(first_name="linguere", last_name="fablab",username="linguerefablab" ,tel_num="+221773146662" ,adress="Senegal" , email="linguerefablab@gmail.com", password="azerty12345")
    print("Superuser créé !")
else:
    print("Superuser existe déjà.")