pip freeze > requirements.txt

./clean_migrations.sh

source ../.env/Scripts/activate

python manage.py makemigrations

python manage.py migrate

git status

git add .

git commit -m "Ajout du fichier requirements.txt. Prochaine etape: Render"

git push -u origin main
