@echo off

REM Lancer Redis dans un terminal
start "" cmd /k "docker run --rm -p 6379:6379 redis:7"

REM Lancer Daphne dans un autre terminal
start "" cmd /k "cd /d C:\Users\7MAKSACOD PC\Desktop\Projet ANTA\AntaBackEnd && set DJANGO_SETTINGS_MODULE=AntaBackEnd.settings && daphne AntaBackEnd.asgi:application"

REM Lancer Django runserver dans un autre terminal
start "" cmd /k "cd /d C:\Users\7MAKSACOD PC\Desktop\Projet ANTA\AntaBackEnd && python manage.py runserver 0.0.0.0:8001"
