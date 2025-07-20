pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

docker run --rm -p 6379:6379 redis:7

DJANGO_SETTINGS_MODULE=AntaBackEnd.settings daphne AntaBackEnd.asgi:application