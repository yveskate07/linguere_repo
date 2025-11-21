#!/bin/bash

# Aller à l'emplacement du script
cd "$(dirname "$0")"

echo "🔍 Nettoyage des migrations Django..."

# Supprimer tous les fichiers de migrations sauf __init__.py
find . -path "*/migrations/*.py" ! -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "🧹 Migrations supprimées."

echo ""
echo "❓ Voulez-vous également supprimer tous les dossiers __pycache__ ? (oui/non)"
read -r answer

# Convertir la réponse en minuscules
answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')

if [ "$answer" = "oui" ]; then
    echo "🔍 Suppression des dossiers __pycache__..."
    find . -type d -name "__pycache__" -exec rm -rf {} +
    echo "🧹 Tous les __pycache__ ont été supprimés."
else
    echo "⏭️ Suppression des __pycache__ ignorée."
fi

echo ""
echo "⚠️ Pensez à recréer les migrations avec :"
echo "python manage.py makemigrations && python manage.py migrate"
