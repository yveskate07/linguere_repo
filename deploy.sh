pip freeze > requirements.txt
python manage.py makemigrations
python manage.py migrate
git add .
git commit -m "deploy"
git push origin yvesBranch
