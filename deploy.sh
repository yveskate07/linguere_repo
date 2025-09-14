pip freeze > requirements.txt
cd AntaBackEnd
python manage.py makemigrations
python manage.py migrate
git add .
git commit -m "Panier Ok Paiement Ok"
git push origin yvesBranch
