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
    User.objects.create_superuser(first_name="linguere", last_name="fablab",username="linguerefablab" ,tel_num="+221773146662" ,adress="Senegal" , email="linguerefablab@gmail.com", password="azerty12345")
    print("Superuser créé !")
else:
    print("Superuser existe déjà.")
    print("Suppression du superuser...")
    # getting the super user with username=linguerefablab
    try:
        superuser = User.objects.get(username="linguerefablab")

    except User.DoesNotExist:
        print("Superuser n'existe pas.")

    else:
        # deleting the super user
        superuser.delete()
        # truncating the table Users_fab_user
        print("Superuser deleted !")
        print("Truncating the table Users_fab_user...")
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE Users_fab_user RESTART IDENTITY CASCADE;")
        # recreating a new superuser
        User.objects.create_superuser(first_name="linguere", last_name="fablab",username="linguerefablab" ,tel_num="+221773146662" ,adress="Senegal" , email="linguerefablab@gmail.com", password="azerty12345")

