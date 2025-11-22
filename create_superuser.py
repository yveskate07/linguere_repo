import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AntaBackEnd.settings")
django.setup()

User = get_user_model()

if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(first_name="linguere", last_name="fablab",username="linguerefablab" ,tel_num="+221773146662" ,adress="Senegal" , email="linguerefablab@gmail.com", password="azerty12345")
    print("Superuser créé !")
else:
    print("Superuser existe déjà.")
